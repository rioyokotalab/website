// Back-to-top button: fade in after scrolling, smooth-scroll to top on click.
// Vanilla JS (no jQuery required).
document.addEventListener('DOMContentLoaded', function () {
	var el = document.getElementById('pagetop');
	if (!el) return;
	el.style.transition = 'opacity 0.3s';
	var toggle = function () {
		var shown = (window.scrollY || document.documentElement.scrollTop) > 100;
		el.style.opacity = shown ? '1' : '0';
		el.style.pointerEvents = shown ? 'auto' : 'none';
	};
	toggle();
	window.addEventListener('scroll', toggle, { passive: true });
	el.addEventListener('click', function (e) {
		e.preventDefault();
		window.scrollTo({ top: 0, behavior: 'smooth' });
	});
});
