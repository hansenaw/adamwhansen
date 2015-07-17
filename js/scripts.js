console.log("Running script...");

$(document).ready(function() {
	$('.bounce').mouseenter(function() {
		$(this).animate({
			height: '+=10px'
		});
	});
	$('.bounce').mouseleave(function() {
		$(this).animate({
			height: '-=10px'
		});
	});
	$('.bounce').click(function() {
		$(this).toggle(1000);
	});
});
