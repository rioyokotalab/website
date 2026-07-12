const { test, expect } = require("@playwright/test");

test("EN/JP contact details use native address semantics without restyling the text", async ({ page }) => {
	for (const language of ["en", "jp"]) {
		await page.goto(`/${language}/contact/index.html`, { waitUntil: "domcontentloaded" });
		const address = page.locator("main address");
		await expect(address).toHaveCount(1);
		expect(await address.evaluate(element => getComputedStyle(element).fontStyle)).toBe("normal");
		expect(await address.textContent()).toContain("rioyokota[at]rio.scrc.iir.isct.ac.jp");
		await expect(address.locator("iframe")).toHaveCount(0);
		await expect(page.locator("main article > p > iframe.location-map")).toHaveCount(1);
	}
});
