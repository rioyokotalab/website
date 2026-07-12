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

test("representative EN/JP page families keep ordered, viewport-contained regions", async ({ page }) => {
	const paths = [
		"/en/index.html", "/jp/index.html", "/en/news/index.html", "/jp/news/index.html",
		"/en/research/index.html", "/jp/research/index.html",
		"/en/computers/index.html", "/jp/computers/index.html",
		"/en/contact/index.html", "/jp/contact/index.html",
		"/en/picture/index.html", "/jp/picture/index.html",
		"/en/member/yokota.html", "/jp/member/yokota.html"
	];
	for (const width of [320, 390, 900, 901, 1200]) {
		await page.setViewportSize({ width, height: 800 });
		for (const path of paths) {
			await page.goto(path, { waitUntil: "domcontentloaded" });
			const geometry = await page.evaluate(() => {
				const selectors = ["#header", "#navbar", "#mainBanner", "#wrapper", "#footer"];
				const regions = selectors.map(selector => {
					const element = document.querySelector(selector);
					const rectangle = element.getBoundingClientRect();
					return {
						selector,
						left: rectangle.left,
						right: rectangle.right,
						top: rectangle.top + scrollY,
						bottom: rectangle.bottom + scrollY,
						visible: rectangle.width > 0 && rectangle.height > 0 && getComputedStyle(element).display !== "none"
					};
				});
				return { documentWidth: document.documentElement.scrollWidth, regions };
			});
			expect(geometry.documentWidth, `${path} at ${width}px`).toBe(width);
			expect(geometry.regions.every(region => region.visible || (width <= 900 && region.selector === "#navbar")), `${path} at ${width}px`).toBe(true);
			expect(geometry.regions.every(region => region.left >= -0.5 && region.right <= width + 0.5), `${path} at ${width}px`).toBe(true);
			for (let index = 1; index < geometry.regions.length; index += 1) {
				expect(geometry.regions[index].top, `${path} at ${width}px: ${geometry.regions[index].selector}`)
					.toBeGreaterThanOrEqual(geometry.regions[index - 1].bottom - 1);
			}
		}
	}
});

test("narrow data tables scroll locally and responsive gallery sources match density", async ({ browser }) => {
	for (const deviceScaleFactor of [1, 2, 3]) {
		const context = await browser.newContext({ baseURL: "http://127.0.0.1:8765", viewport: { width: 390, height: 800 }, deviceScaleFactor });
		await context.addInitScript(([key, value]) => localStorage.setItem(key, value), [storageKey, "rejected"]);
		const page = await context.newPage();
		await page.goto("/en/picture/index.html", { waitUntil: "networkidle" });
		const expectedSuffix = deviceScaleFactor <= 2 ? "-720.jpg" : "-1200.jpg";
		for (const image of await page.locator("#main img").all().then(images => images.slice(0, 7))) {
			await image.scrollIntoViewIfNeeded();
			await image.evaluate(element => element.decode());
			expect(await image.evaluate(element => new URL(element.currentSrc).pathname)).toMatch(new RegExp(`${expectedSuffix.replace(".", "\\.")}$`));
		}
		await context.close();
	}

	const context = await browser.newContext({ baseURL: "http://127.0.0.1:8765", viewport: { width: 320, height: 800 } });
	await context.addInitScript(([key, value]) => localStorage.setItem(key, value), [storageKey, "rejected"]);
	const page = await context.newPage();
	await page.goto("/en/news/index.html", { waitUntil: "networkidle" });
	const table = page.locator("table[tabindex=\"0\"]").first();
	await table.focus();
	await page.keyboard.press("ArrowRight");
	await expect.poll(() => table.evaluate(element => element.scrollLeft)).toBeGreaterThan(0);
	expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBe(320);
	await context.close();
});
