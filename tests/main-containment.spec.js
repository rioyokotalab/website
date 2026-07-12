const { test, expect } = require("@playwright/test");

const routes = [
	"about/index.html", "achievements/index.html", "computers/index.html", "contact/index.html",
	"index.html", "links/index.html", "member/index.html", "member/yokota.html", "news/index.html",
	"picture/index.html", "research/index.html", "software/index.html", "teaching/index.html"
];

test("browser-repaired semantic content remains inside the main landmark", async ({ page }) => {
	for (const language of ["en", "jp"]) {
		for (const route of routes) {
			await page.goto(`/${language}/${route}`, { waitUntil: "domcontentloaded" });
			const result = await page.locator("time, address, iframe, table:not([role='presentation'])").evaluateAll(elements => ({
				count: elements.length,
				outside: elements.filter(element => !element.closest("main")).map(element => element.outerHTML.slice(0, 120))
			}));
			expect(result.outside, `${language}/${route}, ${result.count} semantic elements`).toEqual([]);
		}
	}
});
