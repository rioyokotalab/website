const { test, expect } = require("@playwright/test");

const storageKey = "yokota_analytics_consent_v1";
const galleries = [
	["/en/computers/index.html", "Image viewer", "Close image viewer", "Gallery image 1 of 5"],
	["/en/picture/index.html", "Image viewer", "Close image viewer", "Gallery image 1 of 20"],
	["/en/research/index.html", "Image viewer", "Close image viewer", "Gallery image 1 of 38"],
	["/jp/computers/index.html", "画像ビューア", "画像ビューアを閉じる", "ギャラリー画像（5枚中1枚目）"],
	["/jp/picture/index.html", "画像ビューア", "画像ビューアを閉じる", "ギャラリー画像（21枚中1枚目）"],
	["/jp/research/index.html", "画像ビューア", "画像ビューアを閉じる", "ギャラリー画像（54枚中1枚目）"]
];

test.beforeEach(async ({ page }) => {
	await page.addInitScript(([key, value]) => localStorage.setItem(key, value), [storageKey, "rejected"]);
});

test("galleries expose a localized modal, trap focus, and return it on Escape", async ({ page }) => {
	for (const [path, dialogName, closeName, firstImageName] of galleries) {
		await page.goto(path, { waitUntil: "networkidle" });
		const trigger = page.locator("[data-lightbox]").first();
		await trigger.focus();
		await page.keyboard.press("Enter");

		const dialog = page.getByRole("dialog", { name: dialogName });
		await expect(dialog).toBeVisible();
		const close = page.getByRole("button", { name: closeName });
		await expect(close).toBeFocused({ timeout: 5000 });
		await expect(page.locator(".lb-image")).toHaveAttribute("alt", firstImageName);
		expect(await page.evaluate(() => [...document.body.children]
			.filter(element => element.id !== "lightbox" && element.id !== "lightboxOverlay" && element.tagName !== "SCRIPT")
			.every(element => element.inert))).toBe(true);

		for (let index = 0; index < 4; index += 1) {
			await page.keyboard.press("Tab");
			expect(await page.evaluate(() => document.activeElement.closest("#lightbox") !== null)).toBe(true);
		}

		await page.keyboard.press("ArrowRight");
		await expect(page.locator(".lb-image")).not.toHaveAttribute("alt", firstImageName, { timeout: 5000 });
		await page.keyboard.press("Escape");
		await expect(dialog).toBeHidden();
		await expect(trigger).toBeFocused({ timeout: 5000 });
		expect(await page.evaluate(() => [...document.body.children].every(element => !element.inert))).toBe(true);
	}
});

test("last gallery item exposes previous and close controls only", async ({ page }) => {
	for (const [path, dialogName, closeName] of [galleries[1], galleries[4]]) {
		await page.goto(path, { waitUntil: "networkidle" });
		const trigger = page.locator("[data-lightbox]").last();
		await trigger.focus();
		await page.keyboard.press("Enter");
		await expect(page.getByRole("dialog", { name: dialogName })).toBeVisible();
		await expect(page.getByRole("button", { name: closeName })).toBeFocused({ timeout: 5000 });
		const visibleControls = await page.locator("#lightbox a[role=button]").evaluateAll(elements => elements
			.filter(element => element.getBoundingClientRect().width > 0 && getComputedStyle(element).display !== "none")
			.map(element => element.className));
		expect(visibleControls).toEqual(["lb-prev", "lb-close"]);
		await page.getByRole("button", { name: closeName }).click();
		await expect(trigger).toBeFocused({ timeout: 5000 });
	}
});
