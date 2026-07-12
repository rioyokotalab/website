(() => {
	"use strict";

	const initialize = () => {
		const dialog = document.getElementById("lightbox");
		const overlay = document.getElementById("lightboxOverlay");
		if (!dialog || !overlay) return;

		const japanese = document.documentElement.lang.toLowerCase().startsWith("ja");
		const labels = japanese ? {
			dialog: "画像ビューア", previous: "前の画像", next: "次の画像",
			close: "画像ビューアを閉じる", cancel: "画像の読み込みを中止"
		} : {
			dialog: "Image viewer", previous: "Previous image", next: "Next image",
			close: "Close image viewer", cancel: "Cancel image loading"
		};
		const previous = dialog.querySelector(".lb-prev");
		const next = dialog.querySelector(".lb-next");
		const close = dialog.querySelector(".lb-close");
		const cancel = dialog.querySelector(".lb-cancel");
		const image = dialog.querySelector(".lb-image");
		const number = dialog.querySelector(".lb-number");
		const controls = [previous, next, close, cancel].filter(Boolean);
		let trigger = null;
		let open = false;
		let inerted = [];

		dialog.setAttribute("role", "dialog");
		dialog.setAttribute("aria-modal", "true");
		dialog.setAttribute("aria-label", labels.dialog);
		[[previous, labels.previous], [next, labels.next], [close, labels.close], [cancel, labels.cancel]].forEach(([control, label]) => {
			if (control) {
				control.setAttribute("role", "button");
				control.setAttribute("tabindex", "0");
				control.setAttribute("aria-label", label);
			}
		});

		document.addEventListener("click", (event) => {
			const candidate = event.target.closest("[data-lightbox]");
			if (candidate) trigger = candidate;
		}, true);

		const visibleControls = () => controls.filter((control) => {
			const rectangle = control.getBoundingClientRect();
			return rectangle.width > 0 && rectangle.height > 0 && getComputedStyle(control).display !== "none";
		});

		const updateImageName = () => {
			if (!image || !number) return;
			const match = number.textContent.match(/(\d+)\D+(\d+)/);
			if (!match) return;
			image.alt = japanese ? `ギャラリー画像（${match[2]}枚中${match[1]}枚目）` : `Gallery image ${match[1]} of ${match[2]}`;
		};

		const setBackgroundInert = (value) => {
			if (value) {
				inerted = [...document.body.children]
					.filter((element) => element !== dialog && element !== overlay && element.tagName !== "SCRIPT")
					.map((element) => [element, element.inert]);
				inerted.forEach(([element]) => { element.inert = true; });
			} else {
				inerted.forEach(([element, previousValue]) => { element.inert = previousValue; });
				inerted = [];
			}
		};

		const synchronize = () => {
			const nowOpen = getComputedStyle(dialog).display !== "none";
			updateImageName();
			if (nowOpen && !open) {
				open = true;
				setBackgroundInert(true);
				requestAnimationFrame(() => requestAnimationFrame(() => { (close || dialog).focus(); }));
				setTimeout(() => { (close || dialog).focus(); }, 100);
			} else if (nowOpen && open && close && (document.activeElement === overlay || document.activeElement === document.body)) {
				const rectangle = close.getBoundingClientRect();
				if (rectangle.width > 0 && rectangle.height > 0) close.focus();
			} else if (!nowOpen && open) {
				open = false;
				setBackgroundInert(false);
				const returnTarget = trigger;
				requestAnimationFrame(() => {
					if (returnTarget && returnTarget.isConnected) returnTarget.focus();
				});
				setTimeout(() => {
					if (returnTarget && returnTarget.isConnected) returnTarget.focus();
				}, 100);
			}
		};

		dialog.addEventListener("keydown", (event) => {
			if (event.key !== "Tab" || !open) return;
			const available = visibleControls();
			if (!available.length) {
				event.preventDefault();
				dialog.focus();
				return;
			}
			const first = available[0];
			const last = available[available.length - 1];
			if (event.shiftKey && document.activeElement === first) {
				event.preventDefault();
				last.focus();
			} else if (!event.shiftKey && document.activeElement === last) {
				event.preventDefault();
				first.focus();
			}
		});

		new MutationObserver(synchronize).observe(dialog, {
			attributes: true, attributeFilter: ["style"], characterData: true,
			childList: true, subtree: true
		});
		synchronize();
	};

	const start = () => {
		if (document.getElementById("lightbox")) {
			initialize();
			return;
		}
		const observer = new MutationObserver(() => {
			if (document.getElementById("lightbox")) {
				observer.disconnect();
				initialize();
			}
		});
		observer.observe(document.body, { childList: true });
	};

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", start, { once: true });
	} else {
		start();
	}
})();
