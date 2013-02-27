/*global $, google, window */

/*jshint laxcomma:true */

(function (pore) {
"use strict";

function renderMap(canvasEl, latlng) {
	var ll = latlng.split(',')
	,   gmap = new google.maps.Map(canvasEl, {
			'center': new google.maps.LatLng(parseFloat(ll[0]), parseFloat(ll[1])),
			'zoom': 8,
			'mapTypeId': google.maps.MapTypeId.HYBRID,
			'panControl': false
		});

	new google.maps.Marker({
		'position': gmap.getCenter(),
		'map': gmap,
		'clickable': false
	});
}

function initGallery() {
	$('body').on('click', '.map:not(.show-map) .btn', function () {
		var $btn = $(this)
		,   $canvas = $btn.parents('.map').find('.gmap-canvas');
		$btn.parents('.map').addClass('show-gmap');
		$btn.text('hide map');
		if ($btn.attr('data-ll')) {
			renderMap($canvas.get(0), $btn.attr('data-ll'));
			$btn.removeAttr('data-ll');
		}
		return false;
	}).on('click', '.map.show-gmap .btn', function () {
		$(this)
			.text('show map')
			.parents('.map')
				.removeClass('show-gmap');
		return false;
	});
}

pore.gallery = {
	'init': initGallery
};

}(window.pore));
