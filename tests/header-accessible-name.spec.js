const { test, expect } = require("@playwright/test");

const routes = [
	"about/index.html", "achievements/index.html", "computers/index.html", "contact/index.html",
	"index.html", "links/index.html", "member/index.html", "member/yokota.html", "news/index.html",
	"picture/index.html", "research/index.html", "software/index.html", "teaching/index.html"
];

test("the header logo home link has a localized accessible name on every route", async ({ page }) => {
	for (const [language, name] of [["en", "YOKOTA Laboratory"], ["jp", "横田研究室"]]) {
		for (const route of routes) {
			await page.goto(`/${language}/${route}`, { waitUntil: "domcontentloaded" });
			const logo = page.locator(".htitle > a");
			await expect(logo).toHaveAccessibleName(name);
			await expect(logo.locator(".logomark img")).toHaveAttribute("alt", name);
		}
	}
});
