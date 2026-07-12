(function () {
	"use strict";
	document.documentElement.classList.add("js");

	var control = document.getElementById("menubar_hdr");
	var menu = document.getElementById("menubar-s");
	var mobileNavigation = window.matchMedia("(max-width: 900px)").matches;
	if (!control || !menu || !mobileNavigation) {
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
