const { test, expect } = require("@playwright/test");

test("mirrored achievement citations expose complete arXiv and BibTeX rows", async ({ page }) => {
	for (const language of ["en", "jp"]) {
		await page.goto(`/${language}/achievements/index.html`, { waitUntil: "domcontentloaded" });
		const entries = page.locator("main ol > li");
		const sourced = page.locator('main ol > li[data-url^="https://arxiv.org/abs/"]');
		await expect(entries).toHaveCount(309);
		await expect(sourced).toHaveCount(30);

		for (const entry of await entries.all()) {
			const sourceRows = entry.locator(":scope > .achievement-links");
			const expectedRows = (await entry.getAttribute("data-url") || "")
				.startsWith("https://arxiv.org/abs/") ? 1 : 0;
			await expect(sourceRows).toHaveCount(expectedRows);
			await expect(entry.locator(":scope > br")).toHaveCount(expectedRows);
		}

		for (const entry of await sourced.all()) {
			const identifier = (await entry.getAttribute("data-url")).split("/abs/")[1];
			const row = entry.locator(":scope > .achievement-links");
			const links = row.locator(":scope > a");
			await expect(links).toHaveCount(2);
			await expect(links.nth(0)).toHaveText("[arxiv]");
			await expect(links.nth(0)).toHaveAttribute("href", `https://arxiv.org/abs/${identifier}`);
			await expect(links.nth(1)).toHaveText("[bibtex]");
			await expect(links.nth(1)).toHaveAttribute("href", `https://arxiv.org/bibtex/${identifier}`);
			for (const link of await links.all()) {
				await expect(link).toHaveAttribute("target", "_blank");
				await expect(link).toHaveAttribute("rel", "noopener noreferrer");
			}
			expect(await row.evaluate((element) => element.previousElementSibling?.tagName)).toBe("BR");
		}
	}
});
