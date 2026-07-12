const { test, expect } = require("@playwright/test");

test("mirrored cluster specification tables have localized native names", async ({ page }) => {
	for (const [language, name] of [["en", "Hinadori cluster hardware"], ["jp", "ひなどりクラスタのハードウェア"]]) {
		await page.goto(`/${language}/computers/index.html`, { waitUntil: "domcontentloaded" });
		const table = page.getByRole("table", { name, exact: true });
		await expect(table).toHaveCount(1);
		await expect(table.locator("caption")).toHaveClass("visually-hidden");
		expect(await table.getByRole("columnheader").count()).toBe(4);
		const captionBox = await table.locator("caption").boundingBox();
		expect(captionBox.width).toBe(1);
		expect(captionBox.height).toBe(1);
	}
});
