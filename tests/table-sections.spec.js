const { test, expect } = require("@playwright/test");

test("news tables contain no empty rendered row groups", async ({ page }) => {
	for (const language of ["en", "jp"]) {
		await page.goto(`/${language}/news/index.html`, { waitUntil: "domcontentloaded" });
		await expect(page.locator("table tbody:empty")).toHaveCount(0);
		const tables = page.locator("main table");
		for (const table of await tables.all()) {
			expect(await table.locator("tr").count()).toBeGreaterThan(0);
		}
	}
});
