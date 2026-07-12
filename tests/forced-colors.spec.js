const { test, expect } = require("@playwright/test");

const storageKey = "yokota_analytics_consent_v1";

const focusByKeyboard = async (page, locator, key = "Tab", limit = 200) => {
	for (let index = 0; index < limit; index += 1) {
		await page.keyboard.press(key);
		if (await locator.evaluate(element => document.activeElement === element)) return;
	}
	throw new Error(`keyboard focus did not reach ${await locator.evaluate(element => element.outerHTML)}`);
};

test("forced colors preserves current, focus, link, and consent distinctions in EN and JP", async ({ browser }) => {
	const context = await browser.newContext({
		baseURL: "http://127.0.0.1:8765", forcedColors: "active", viewport: { width: 1200, height: 800 }
	});
	const page = await context.newPage();
	for (const path of ["/en/research/index.html", "/jp/research/index.html"]) {
		await page.goto(path);
		const current = page.locator("#menubar a[aria-current=\"page\"]");
		await expect(current).toBeVisible();
		expect(await current.evaluate(element => getComputedStyle(element).outlineStyle)).toBe("solid");
		expect(await current.evaluate(element => getComputedStyle(element).outlineWidth)).toBe("2px");
		await focusByKeyboard(page, current);
		expect(await current.evaluate(element => getComputedStyle(element).outlineWidth)).toBe("3px");
		expect(await current.evaluate(element => getComputedStyle(element).boxShadow)).toBe("none");
		const contentLink = page.locator("#main a").first();
		await expect(contentLink).toBeVisible();
		expect(await contentLink.evaluate(element => getComputedStyle(element).textDecorationLine)).toContain("underline");
		const consent = page.locator("#analytics-consent");
		await expect(consent).toBeVisible();
		for (const button of await consent.locator("button").all()) {
			await expect(button).toBeVisible();
			await button.focus();
			expect(await button.evaluate(element => getComputedStyle(element).outlineWidth)).toBe("3px");
		}
	}
	await context.close();
});

test("forced colors keeps mobile menus, local tables, and EN/JP galleries operable", async ({ browser }) => {
	const context = await browser.newContext({
		baseURL: "http://127.0.0.1:8765", forcedColors: "active", viewport: { width: 320, height: 800 }
	});
	await context.addInitScript(([key, value]) => localStorage.setItem(key, value), [storageKey, "rejected"]);
	const page = await context.newPage();
	for (const path of ["/en/news/index.html", "/jp/news/index.html"]) {
		await page.goto(path);
		const menuButton = page.locator("#menubar_hdr");
		await menuButton.click();
		await expect(page.locator("#menubar-s")).toBeVisible();
		await focusByKeyboard(page, menuButton, "Shift+Tab");
		expect(await menuButton.evaluate(element => getComputedStyle(element).outlineWidth)).toBe("3px");
		const table = page.locator("table[tabindex=\"0\"]").first();
		await focusByKeyboard(page, table);
		await page.keyboard.press("ArrowRight");
		await expect.poll(() => table.evaluate(element => element.scrollLeft)).toBeGreaterThan(0);
		expect(await table.evaluate(element => getComputedStyle(element).outlineWidth)).toBe("3px");
		expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBe(320);
	}
	for (const path of ["/en/picture/index.html", "/jp/picture/index.html"]) {
		await page.goto(path);
		const trigger = page.locator("[data-lightbox]").first();
		await focusByKeyboard(page, trigger);
		await page.keyboard.press("Enter");
		const close = page.locator(".lb-close");
		await expect(close).toBeFocused();
		expect(await close.evaluate(element => getComputedStyle(element).outlineWidth)).toBe("3px");
		await page.keyboard.press("Escape");
		await expect(page.locator("#lightbox")).toBeHidden();
	}
	await context.close();
});
