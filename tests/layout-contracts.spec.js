const { test, expect } = require("@playwright/test");

const storageKey = "yokota_analytics_consent_v1";

test.beforeEach(async ({ page }) => {
	await page.addInitScript(([key, value]) => localStorage.setItem(key, value), [storageKey, "rejected"]);
});

test("responsive navigation switches cleanly at 900/901px in EN and JP", async ({ page }) => {
	for (const width of [900, 901]) {
		await page.setViewportSize({ width, height: 800 });
		for (const path of ["/en/about/index.html", "/jp/about/index.html"]) {
			await page.goto(path);
			const button = page.locator("#menubar_hdr");
			const desktop = page.locator("#menubar");
			const mobile = page.locator("#menubar-s");
			if (width === 900) {
				await expect(button).toBeVisible();
				await expect(desktop).toBeHidden();
				await expect(mobile).toBeHidden();
				await button.click();
				await expect(mobile).toBeVisible();
				await expect(button).toHaveAttribute("aria-expanded", "true");
				await button.click();
				await expect(mobile).toBeHidden();
			} else {
				await expect(button).toBeHidden();
				await expect(desktop).toBeVisible();
				await expect(mobile).toBeHidden();
			}
			expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBe(width);
		}
	}
});

test("print media is content-first and free of horizontal overflow", async ({ page }) => {
	await page.setViewportSize({ width: 794, height: 1123 });
	await page.emulateMedia({ media: "print" });
	for (const path of [
		"/en/index.html", "/jp/index.html", "/en/news/index.html", "/jp/research/index.html",
		"/en/contact/index.html", "/jp/picture/index.html"
	]) {
		await page.goto(path);
		for (const selector of [
			"#header", "#navbar", "#sub", "#footer", "#pagetop", "#menubar_hdr",
			".analytics-consent-settings", ".location-map"
		]) {
			await expect(page.locator(selector)).toBeHidden();
		}
		await expect(page.locator("#mainBanner .slogan")).toBeVisible();
		await expect(page.locator("#mainBanner img")).toBeHidden();
		expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(794);
		expect(await page.evaluate(() => [...document.querySelectorAll("#main *")]
			.every(element => element.getBoundingClientRect().right <= innerWidth + 0.5))).toBe(true);
	}
});
