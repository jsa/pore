$.ajaxSetup({'traditional': true});

window.pore = window.pore || {};

$(function () {
	// navigation handling
	$('.navbar .nav a[href="' + window.location.pathname + '"]').parent().addClass('active');
});
