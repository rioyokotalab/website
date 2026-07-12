const { test, expect } = require("@playwright/test");

const routes = [
	"about/index.html", "achievements/index.html", "computers/index.html", "contact/index.html",
	"index.html", "links/index.html", "member/index.html", "member/yokota.html", "news/index.html",
	"picture/index.html", "research/index.html", "software/index.html", "teaching/index.html"
];

test("every route exposes only purposeful, localized images", async ({ page }) => {
	for (const language of ["en", "jp"]) {
		for (const route of routes) {
			await page.goto(`/${language}/${route}`, { waitUntil: "domcontentloaded" });
			const names = await page.getByRole("img").evaluateAll(images =>
				images.map(image => image.getAttribute("alt"))
			);
			const expected = [language === "en" ? "YOKOTA Laboratory" : "横田研究室"];
			if (route === "member/yokota.html") {
				expected.push(language === "en" ? "Professor Rio Yokota" : "横田理央教授");
			}
			expect(names).toEqual(expected);
		}
	}
});
