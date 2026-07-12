const { test, expect } = require("@playwright/test");

const routes = [
	"about/index.html", "achievements/index.html", "computers/index.html", "contact/index.html",
	"index.html", "links/index.html", "member/index.html", "member/yokota.html", "news/index.html",
	"picture/index.html", "research/index.html", "software/index.html", "teaching/index.html"
];

test("every rendered data table has a nonempty, route-unique accessible name", async ({ page }) => {
	for (const language of ["en", "jp"]) {
		for (const route of routes) {
			await page.goto(`/${language}/${route}`, { waitUntil: "domcontentloaded" });
			const tables = page.getByRole("table");
			const expectedCount = route === "news/index.html" ? 12 : ["index.html", "computers/index.html", "member/index.html"].includes(route) ? 1 : 0;
			await expect(tables).toHaveCount(expectedCount);
			const names = [];
			for (const table of await tables.all()) {
				const firstLine = (await table.ariaSnapshot()).split("\n", 1)[0];
				const match = firstLine.match(/^- table "(.+)":?$/);
				expect(match, `${language}/${route}: ${firstLine}`).not.toBeNull();
				names.push(match[1]);
			}
			expect(new Set(names).size).toBe(names.length);
		}
	}
});
