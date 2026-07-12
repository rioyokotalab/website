const { test, expect } = require("@playwright/test");

const routes = [
	"about/index.html", "achievements/index.html", "computers/index.html",
	"contact/index.html", "index.html", "links/index.html", "member/index.html",
	"member/yokota.html", "news/index.html", "picture/index.html",
	"research/index.html", "software/index.html", "teaching/index.html"
];

test("all routes retain content, navigation, and local gallery links without JavaScript", async ({ browser }) => {
	for (const width of [320, 1200]) {
		const context = await browser.newContext({
			baseURL: "http://127.0.0.1:8765",
			javaScriptEnabled: false,
			viewport: { width, height: 800 }
		});
		const page = await context.newPage();
		for (const language of ["en", "jp"]) {
			for (const route of routes) {
				const path = `/${language}/${route}`;
				await page.goto(path, { waitUntil: "domcontentloaded" });
				expect((await page.locator("#wrapper").innerText()).trim().length, `${path} content`).toBeGreaterThan(0);
				expect(await page.evaluate(() => document.documentElement.scrollWidth), path).toBe(width);
				await expect(page.locator("#menubar_hdr"), `${path} inert control`).toBeHidden();
				if (width <= 900) {
					await expect(page.locator("#menubar")).toBeHidden();
					await expect(page.locator("#menubar-s")).toBeVisible();
				} else {
					await expect(page.locator("#menubar")).toBeVisible();
					await expect(page.locator("#menubar-s")).toBeHidden();
				}
				const galleryTargets = await page.locator("[data-lightbox]").evaluateAll(elements => elements.map(element => new URL(element.href).pathname));
				expect(galleryTargets.every(target => /\.(?:jpe?g|png)$/i.test(target))).toBe(true);
				await expect(page.locator('link[rel="canonical"]')).toHaveCount(1);
			}
		}
		await context.close();
	}
});

test("root entry exposes both language choices without JavaScript", async ({ browser }) => {
	const context = await browser.newContext({
		baseURL: "http://127.0.0.1:8765",
		javaScriptEnabled: false,
		viewport: { width: 390, height: 800 }
	});
	const page = await context.newPage();
	await page.goto("/index.html");
	await expect(page.getByRole("link", { name: "English" })).toBeVisible();
	await expect(page.getByRole("link", { name: "日本語" })).toBeVisible();
	await context.close();
});
