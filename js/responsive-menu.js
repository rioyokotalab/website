(function () {
	"use strict";

	var control = document.getElementById("menubar_hdr");
	var menu = document.getElementById("menubar-s");
	var viewportWidth = Math.min(window.screen.width, window.innerWidth);
	if (!control || !menu || viewportWidth > 800) {
		return;
	}

	function setExpanded(expanded) {
		menu.classList.toggle("is-collapsed", !expanded);
		control.classList.toggle("open", expanded);
		control.classList.toggle("close", !expanded);
		control.setAttribute("aria-expanded", String(expanded));
	}

	control.addEventListener("click", function () {
		setExpanded(control.getAttribute("aria-expanded") !== "true");
	});
	setExpanded(false);
})();
