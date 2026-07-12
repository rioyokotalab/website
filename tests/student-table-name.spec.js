const { test, expect } = require("@playwright/test");

test("active-student tables use localized headings while layout tables stay presentational", async ({ page }) => {
	for (const [language, name] of [["en", "Students"], ["jp", "学生"]]) {
		await page.goto(`/${language}/member/index.html`, { waitUntil: "domcontentloaded" });
		const table = page.getByRole("table", { name, exact: true });
		await expect(table).toHaveCount(1);
		await expect(table).toHaveAttribute("aria-labelledby", "sub002");
		await expect(page.getByRole("table")).toHaveCount(1);
		await expect(page.locator('table[role="presentation"]')).toHaveCount(3);
	}
});
