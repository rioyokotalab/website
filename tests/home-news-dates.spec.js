const { test, expect } = require("@playwright/test");

test("mirrored home-news dates expose valid ISO values without changing text", async ({ page }) => {
	for (const language of ["en", "jp"]) {
		await page.goto(`/${language}/index.html`, { waitUntil: "domcontentloaded" });
		const dates = await page.locator("time").evaluateAll(elements => elements.map(element => ({
			iso: element.getAttribute("datetime"),
			visible: element.textContent
		})));
		expect(dates).toHaveLength(language === "en" ? 32 : 14);
		for (const item of dates) {
			expect(item.visible).toBe(item.iso.replaceAll("-", "."));
			expect(Number.isNaN(Date.parse(`${item.iso}T00:00:00Z`))).toBe(false);
		}
	}
});
