const { test, expect } = require("@playwright/test");

const storageKey = "yokota_analytics_consent_v1";

const maximumDuration = async (page) => page.evaluate(() => {
	const seconds = (value) => value.split(",").map(item => {
		const duration = Number.parseFloat(item);
		return item.trim().endsWith("ms") ? duration / 1000 : duration;
	});
	return Math.max(0, ...[...document.querySelectorAll("*")].flatMap(element => {
		const style = getComputedStyle(element);
		return [...seconds(style.transitionDuration), ...seconds(style.animationDuration)];
	}));
});

test("reduced-motion preference makes page and gallery state changes immediate", async ({ browser }) => {
	const context = await browser.newContext({ reducedMotion: "reduce", viewport: { width: 390, height: 800 } });
	await context.addInitScript(([key, value]) => localStorage.setItem(key, value), [storageKey, "rejected"]);
	const page = await context.newPage();
	await page.goto("/en/picture/index.html");
	await expect.poll(() => maximumDuration(page)).toBeLessThanOrEqual(0.001);
	expect(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior)).toBe("auto");
	expect(await page.evaluate(() => ({
		fade: window.lightbox.options.fadeDuration,
		image: window.lightbox.options.imageFadeDuration,
		resize: window.lightbox.options.resizeDuration
	}))).toEqual({ fade: 0, image: 0, resize: 0 });
	await page.locator("[data-lightbox]").first().click();
	await expect(page.locator("#lightbox")).toBeVisible();
	await expect.poll(() => maximumDuration(page)).toBeLessThanOrEqual(0.001);
	await context.close();
});

test("ordinary motion timings remain unchanged without the preference", async ({ browser }) => {
	const context = await browser.newContext({ reducedMotion: "no-preference" });
	await context.addInitScript(([key, value]) => localStorage.setItem(key, value), [storageKey, "rejected"]);
	const page = await context.newPage();
	await page.goto("/en/picture/index.html");
	expect(await page.evaluate(() => ({
		fade: window.lightbox.options.fadeDuration,
		image: window.lightbox.options.imageFadeDuration,
		resize: window.lightbox.options.resizeDuration
	}))).toEqual({ fade: 600, image: 600, resize: 700 });
	expect(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior)).toBe("smooth");
	await page.emulateMedia({ reducedMotion: "reduce" });
	await expect.poll(() => page.evaluate(() => window.lightbox.options.resizeDuration)).toBe(0);
	await page.emulateMedia({ reducedMotion: "no-preference" });
	await expect.poll(() => page.evaluate(() => window.lightbox.options.resizeDuration)).toBe(700);
	await context.close();
});
