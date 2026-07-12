(function () {
	"use strict";

	var measurementId = "G-DVRGG7FDLX";
	var storageKey = "yokota_analytics_consent_v1";
	var accepted = "accepted";
	var rejected = "rejected";
	var analyticsLoaded = false;

	function readChoice() {
		try {
			var choice = window.localStorage.getItem(storageKey);
			return choice === accepted || choice === rejected ? choice : null;
		} catch (error) {
			return null;
		}
	}

	function saveChoice(choice) {
		try {
			window.localStorage.setItem(storageKey, choice);
		} catch (error) {
			/* A blocked localStorage means the choice is requested again next time. */
		}
	}

	function gtag() {
		window.dataLayer.push(arguments);
	}

	function enableAnalytics() {
		if (analyticsLoaded) {
			return;
		}
		analyticsLoaded = true;
		window.dataLayer = window.dataLayer || [];
		window.gtag = gtag;
		gtag("consent", "default", {
			ad_storage: "denied",
			ad_user_data: "denied",
			ad_personalization: "denied",
			analytics_storage: "denied"
		});
		gtag("consent", "update", {
			ad_storage: "denied",
			ad_user_data: "denied",
			ad_personalization: "denied",
			analytics_storage: "granted"
		});
		gtag("js", new Date());
		gtag("config", measurementId);

		var script = document.createElement("script");
		script.async = true;
		script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(measurementId);
		document.head.appendChild(script);
	}

	function removeAnalyticsCookies() {
		var hostname = window.location.hostname;
		var domains = ["", hostname, "." + hostname];
		document.cookie.split(";").forEach(function (item) {
			var name = item.split("=")[0].trim();
			if (name === "_ga" || name.indexOf("_ga_") === 0) {
				domains.forEach(function (domain) {
					var domainPart = domain ? "; domain=" + domain : "";
					document.cookie = name + "=; Max-Age=0; path=/" + domainPart + "; SameSite=Lax";
				});
			}
		});
	}

	function languageText() {
		if ((document.documentElement.lang || "").toLowerCase().indexOf("ja") === 0) {
			return {
				title: "アクセス解析について",
				body: "当サイトは、利用状況を把握して改善するため、同意いただいた場合にのみ Google Analytics を使用します。選択はこのブラウザに保存され、いつでも変更できます。",
				privacy: "Google プライバシーポリシー",
				accept: "同意する",
				reject: "同意しない",
				settings: "プライバシー設定",
				label: "アクセス解析の同意設定"
			};
		}
		return {
			title: "Analytics and privacy",
			body: "We use Google Analytics to understand site usage and improve this website, but only if you consent. Your choice is stored in this browser and can be changed at any time.",
			privacy: "Google Privacy Policy",
			accept: "Accept analytics",
			reject: "Reject analytics",
			settings: "Privacy settings",
			label: "Analytics consent settings"
		};
	}

	function makeButton(text, className, handler) {
		var button = document.createElement("button");
		button.type = "button";
		button.className = className;
		button.textContent = text;
		button.addEventListener("click", handler);
		return button;
	}

	function hideBanner() {
		var banner = document.getElementById("analytics-consent");
		if (banner) {
			banner.remove();
		}
		var settings = document.getElementById("analytics-consent-settings");
		if (settings) {
			settings.hidden = false;
		}
	}

	function rejectAnalytics() {
		var wasLoaded = analyticsLoaded;
		saveChoice(rejected);
		if (wasLoaded && window.gtag) {
			window.gtag("consent", "update", {
				ad_storage: "denied",
				ad_user_data: "denied",
				ad_personalization: "denied",
				analytics_storage: "denied"
			});
		}
		removeAnalyticsCookies();
		hideBanner();
		if (wasLoaded) {
			window.location.reload();
		}
	}

	function acceptAnalytics() {
		saveChoice(accepted);
		enableAnalytics();
		hideBanner();
	}

	function showBanner() {
		if (document.getElementById("analytics-consent")) {
			return;
		}
		var text = languageText();
		var banner = document.createElement("section");
		banner.id = "analytics-consent";
		banner.className = "analytics-consent";
		banner.setAttribute("aria-label", text.label);

		var copy = document.createElement("div");
		copy.className = "analytics-consent-copy";
		var title = document.createElement("h2");
		title.textContent = text.title;
		var paragraph = document.createElement("p");
		paragraph.appendChild(document.createTextNode(text.body + " "));
		var privacy = document.createElement("a");
		privacy.href = "https://policies.google.com/privacy";
		privacy.target = "_blank";
		privacy.rel = "noopener noreferrer";
		privacy.textContent = text.privacy;
		paragraph.appendChild(privacy);
		copy.appendChild(title);
		copy.appendChild(paragraph);

		var actions = document.createElement("div");
		actions.className = "analytics-consent-actions";
		actions.appendChild(makeButton(text.reject, "analytics-consent-reject", rejectAnalytics));
		actions.appendChild(makeButton(text.accept, "analytics-consent-accept", acceptAnalytics));
		banner.appendChild(copy);
		banner.appendChild(actions);
		document.body.appendChild(banner);

		var settings = document.getElementById("analytics-consent-settings");
		if (settings) {
			settings.hidden = true;
		}
		banner.querySelector("button").focus();
	}

	function addSettingsButton() {
		if (document.getElementById("analytics-consent-settings")) {
			return;
		}
		var text = languageText();
		var settings = makeButton(text.settings, "analytics-consent-settings", showBanner);
		settings.id = "analytics-consent-settings";
		settings.hidden = readChoice() === null;
		document.body.appendChild(settings);
	}

	if (readChoice() === accepted) {
		enableAnalytics();
	}

	function initializeInterface() {
		addSettingsButton();
		if (readChoice() === null) {
			showBanner();
		}
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", initializeInterface);
	} else {
		initializeInterface();
	}
}());
