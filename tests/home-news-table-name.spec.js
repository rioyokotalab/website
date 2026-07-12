const { test, expect } = require("@playwright/test");

test("home-news tables have localized native names without visible captions", async ({ page }) => {
	for (const [language, name] of [["en", "News"], ["jp", "ニュース"]]) {
		await page.goto(`/${language}/index.html`, { waitUntil: "domcontentloaded" });
		const table = page.getByRole("table", { name, exact: true });
		await expect(table).toHaveCount(1);
		await expect(table.locator("caption")).toHaveClass("visually-hidden");
		const captionBox = await table.locator("caption").boundingBox();
		expect(captionBox.width).toBe(1);
		expect(captionBox.height).toBe(1);
		expect(await table.getByRole("rowheader").count()).toBe(language === "en" ? 33 : 15);
	}
});
