/*global $, document, FileReader, google, navigator, window */

/*jshint laxcomma:true */

(function (pore) {
"use strict";

var gmap = null;

// I can't seem to get the 'unused' warning suppressed without applying
// suppression globally
function initGMap() {
	var latlng = $('input[name="latlng"]').val()
	,   mapParams = {
			'center': new google.maps.LatLng(11.673755, 102.219543),
			'zoom': 1,
			'mapTypeId': google.maps.MapTypeId.HYBRID,
			'panControl': false
		};

	if (latlng) {
		var ll = latlng.split(',');
		// update params if latlng already defined
		mapParams.center = new google.maps.LatLng(parseFloat(ll[0]), parseFloat(ll[1]));
		mapParams.zoom = 8;
	}

	gmap = new google.maps.Map(document.getElementById('gmap-canvas'), mapParams);

	var marker = new google.maps.Marker({
			'position': gmap.getCenter(),
			'map': gmap,
			'clickable': false
		});

	google.maps.event.addListener(gmap, 'center_changed', function () {
		marker.setPosition(gmap.getCenter());
	});

	// callbacks didn't seem to work on Firefox, so just adjusting map in case
	// Firefox sees it worthwile to invoke a callback
	if (!latlng && navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function(pos) {
			gmap.setCenter(new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude));
			gmap.setZoom(8);
		});
	}
}

function handleFileSelect(evt) {
	var $preview = $('form .thumbnails');
	$preview.empty();
	$.each(evt.target.files, function (i, file) {
		if (!file.type.match('image.*')) {
			return;
		}
		var reader = new FileReader();
		reader.onload = (function(_file) {
			return function(e) {
				$preview.append(
					'<li class="span3"><div class="thumbnail">' +
					'<img src="' + e.target.result + '" ' +
					'title="' + window.escape(_file.name) + '">' +
					'</div></li>');
			};
		})(file);
		reader.readAsDataURL(file);
	});
}

function initUpload() {
	if (typeof FileReader !== 'undefined') {
		document
			.getElementById('file-select')
			.addEventListener('change',
				function (evt) {
					try {
						handleFileSelect(evt);
					} catch (e) { }
				},
				false);
	}

	var $canvas = $('#gmap-canvas');

	$('input[name="gmap-location"]').change(function () {
		if ($(this).is(':checked')) {
			$canvas.css('display', 'block');
			if (!gmap) {
				var script = document.createElement('script');
				script.type = 'text/javascript';
				script.src = 'https://maps.googleapis.com/maps/api/js?key=' + pore.env.GOOGLE_API_KEY + '&sensor=true&callback=pore.upload.initGMap';
				document.body.appendChild(script);
			}
		} else {
			$canvas.css('display', 'none');
		}
	// trigger map loading (may be already populated if form errored)
	}).change();

	$('form').submit(function () {
		var $form = $(this)
		,   postUrl = null;
		function fetchUrl() {
			$.ajax('/upload-url/', {
				'type': 'POST',
				'async': false,
				'dataType': 'json',
				// had to change to submit data already here as unicode values
				// didn't quite survive the blobstore process
				'data': $form.find(':input:not([type="file"])').fieldSerialize(),
				'success': function (data) {
					postUrl = data.url;
				},
				'error': fetchUrl
			});
		}
		fetchUrl();
		if (!postUrl) {
			window.alert(
				"I'm unbelievably sorry, but there seems to be a problem " +
				"with photo uploading currently. I recommend retrying again later.");
			return false;
		}
		this.action = postUrl;
		if (gmap) {
			$('input[name="latlng"]').val(gmap.getCenter().toUrlValue());
		}
		return true;
	});
}

pore.upload = {
	'init': initUpload,
	'initGMap': initGMap
};

}(window.pore));
