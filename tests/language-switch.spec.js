const { test, expect } = require("@playwright/test");

const routes = [
	"about/index.html", "achievements/index.html", "computers/index.html", "contact/index.html",
	"index.html", "links/index.html", "member/index.html", "member/yokota.html", "news/index.html",
	"picture/index.html", "research/index.html", "software/index.html", "teaching/index.html"
];

test("every route identifies its exact alternate-language destination", async ({ page }) => {
	for (const language of ["en", "jp"]) {
		const destination = language === "en" ? "jp" : "en";
		const label = language === "en" ? "JAPANESE" : "ENGLISH";
		const hreflang = language === "en" ? "ja" : "en";
		for (const route of routes) {
			await page.goto(`/${language}/${route}`, { waitUntil: "domcontentloaded" });
			const link = page.getByRole("link", { name: label, exact: true });
			await expect(link).toHaveCount(1);
			await expect(link).toHaveAttribute("hreflang", hreflang);
			await expect(link).toHaveAttribute("href", route === "index.html" ? `../${destination}/index.html` : `../../${destination}/${route}`);
		}
	}
});
