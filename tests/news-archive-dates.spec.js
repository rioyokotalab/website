const { test, expect } = require("@playwright/test");

test("single-day archive dates expose ISO values while ranges remain plain text", async ({ page }) => {
	for (const language of ["en", "jp"]) {
		await page.goto(`/${language}/news/index.html`, { waitUntil: "domcontentloaded" });
		const dates = await page.locator("time").evaluateAll(elements => elements.map(element => ({
			iso: element.getAttribute("datetime"),
			visible: element.textContent
		})));
		expect(dates).toHaveLength(language === "en" ? 96 : 100);
		for (const item of dates) {
			const normalizedVisible = item.visible.split(".").map((part, index) => index === 0 ? part : part.padStart(2, "0")).join("-");
			expect(item.iso).toBe(normalizedVisible);
			expect(Number.isNaN(Date.parse(`${item.iso}T00:00:00Z`))).toBe(false);
		}
		const rangedHeaders = page.getByRole("rowheader").filter({ hasText: /^\d{4}\.\d{1,2}\.\d{1,2}-\d{1,2}\s*$/ });
		await expect(rangedHeaders).toHaveCount(2);
		await expect(rangedHeaders.locator("time")).toHaveCount(0);
	}
});
