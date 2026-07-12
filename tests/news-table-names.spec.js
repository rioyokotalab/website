const { test, expect } = require("@playwright/test");

test("every archive table has a localized contextual name", async ({ page }) => {
	for (const language of ["en", "jp"]) {
		await page.goto(`/${language}/news/index.html`, { waitUntil: "domcontentloaded" });
		for (let year = 2026; year >= 2016; year -= 1) {
			const name = language === "en" ? `${year}` : `${year}年`;
			const table = page.getByRole("table", { name, exact: true });
			await expect(table).toHaveCount(1);
			await expect(table).toHaveAttribute("aria-labelledby", `Y${year}`);
		}
		const seminarName = language === "en" ? "Seminar details" : "セミナー詳細";
		await expect(page.getByRole("table", { name: seminarName, exact: true })).toHaveCount(1);
		await expect(page.getByRole("table")).toHaveCount(12);
	}
});
