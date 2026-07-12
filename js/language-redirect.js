(function () {
	"use strict";

	var language = (navigator.language || navigator.userLanguage || "").slice(0, 2);
	window.location.replace(language === "en" ? "en/index.html" : "jp/index.html");
})();
