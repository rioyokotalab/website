// Back-to-top button: fade in after scrolling, smooth-scroll to top on click.
// Vanilla JS (no jQuery required).
document.addEventListener('DOMContentLoaded', function () {
	var el = document.getElementById('pagetop');
	if (!el) return;
	var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
	el.classList.toggle('reduce-motion', reducedMotion);
	var toggle = function () {
		var shown = (window.scrollY || document.documentElement.scrollTop) > 100;
		el.classList.toggle('is-visible', shown);
	};
	toggle();
	window.addEventListener('scroll', toggle, { passive: true });
	el.addEventListener('click', function (e) {
		e.preventDefault();
		window.scrollTo({ top: 0, behavior: reducedMotion ? 'auto' : 'smooth' });
	});
});
