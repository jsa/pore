$.ajaxSetup({'traditional': true});

window.pore = window.pore || {};

$(function () {
	// navigation handling
	$('.navbar .nav a[href="' + window.location.pathname + '"]').parent().addClass('active');
});
/* =============================================================
 * bootstrap-collapse.js v2.3.0
 * http://twitter.github.com/bootstrap/javascript.html#collapse
 * =============================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ============================================================ */


!function ($) {

  "use strict"; // jshint ;_;


 /* COLLAPSE PUBLIC CLASS DEFINITION
  * ================================ */

  var Collapse = function (element, options) {
    this.$element = $(element)
    this.options = $.extend({}, $.fn.collapse.defaults, options)

    if (this.options.parent) {
      this.$parent = $(this.options.parent)
    }

    this.options.toggle && this.toggle()
  }

  Collapse.prototype = {

    constructor: Collapse

  , dimension: function () {
      var hasWidth = this.$element.hasClass('width')
      return hasWidth ? 'width' : 'height'
    }

  , show: function () {
      var dimension
        , scroll
        , actives
        , hasData

      if (this.transitioning || this.$element.hasClass('in')) return

      dimension = this.dimension()
      scroll = $.camelCase(['scroll', dimension].join('-'))
      actives = this.$parent && this.$parent.find('> .accordion-group > .in')

      if (actives && actives.length) {
        hasData = actives.data('collapse')
        if (hasData && hasData.transitioning) return
        actives.collapse('hide')
        hasData || actives.data('collapse', null)
      }

      this.$element[dimension](0)
      this.transition('addClass', $.Event('show'), 'shown')
      $.support.transition && this.$element[dimension](this.$element[0][scroll])
    }

  , hide: function () {
      var dimension
      if (this.transitioning || !this.$element.hasClass('in')) return
      dimension = this.dimension()
      this.reset(this.$element[dimension]())
      this.transition('removeClass', $.Event('hide'), 'hidden')
      this.$element[dimension](0)
    }

  , reset: function (size) {
      var dimension = this.dimension()

      this.$element
        .removeClass('collapse')
        [dimension](size || 'auto')
        [0].offsetWidth

      this.$element[size !== null ? 'addClass' : 'removeClass']('collapse')

      return this
    }

  , transition: function (method, startEvent, completeEvent) {
      var that = this
        , complete = function () {
            if (startEvent.type == 'show') that.reset()
            that.transitioning = 0
            that.$element.trigger(completeEvent)
          }

      this.$element.trigger(startEvent)

      if (startEvent.isDefaultPrevented()) return

      this.transitioning = 1

      this.$element[method]('in')

      $.support.transition && this.$element.hasClass('collapse') ?
        this.$element.one($.support.transition.end, complete) :
        complete()
    }

  , toggle: function () {
      this[this.$element.hasClass('in') ? 'hide' : 'show']()
    }

  }


 /* COLLAPSE PLUGIN DEFINITION
  * ========================== */

  var old = $.fn.collapse

  $.fn.collapse = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('collapse')
        , options = $.extend({}, $.fn.collapse.defaults, $this.data(), typeof option == 'object' && option)
      if (!data) $this.data('collapse', (data = new Collapse(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.collapse.defaults = {
    toggle: true
  }

  $.fn.collapse.Constructor = Collapse


 /* COLLAPSE NO CONFLICT
  * ==================== */

  $.fn.collapse.noConflict = function () {
    $.fn.collapse = old
    return this
  }


 /* COLLAPSE DATA-API
  * ================= */

  $(document).on('click.collapse.data-api', '[data-toggle=collapse]', function (e) {
    var $this = $(this), href
      , target = $this.attr('data-target')
        || e.preventDefault()
        || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '') //strip for ie7
      , option = $(target).data('collapse') ? 'toggle' : $this.data()
    $this[$(target).hasClass('in') ? 'addClass' : 'removeClass']('collapsed')
    $(target).collapse(option)
  })

}(window.jQuery);/*global $, google, window */

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
		var postUrl = null;
		function fetchUrl() {
			$.ajax('/upload-url/', {
				'async': false,
				'dataType': 'json',
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
