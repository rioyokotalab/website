(() => {
	"use strict";

	const update = () => {
		document.querySelectorAll(".mobile-table-containment table").forEach((table) => {
			if (table.scrollWidth > table.clientWidth + 1) {
				table.setAttribute("tabindex", "0");
			} else {
				table.removeAttribute("tabindex");
			}
		});
	};

	update();
	window.addEventListener("resize", update, { passive: true });
})();
