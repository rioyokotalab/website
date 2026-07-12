const { test, expect } = require("@playwright/test");

const storageKey = "yokota_analytics_consent_v1";
const routes = [
	"/en/about/index.html", "/en/achievements/index.html", "/en/computers/index.html",
	"/en/contact/index.html", "/en/index.html", "/en/links/index.html", "/en/member/index.html",
	"/en/member/yokota.html", "/en/news/index.html", "/en/picture/index.html",
	"/en/research/index.html", "/en/software/index.html", "/en/teaching/index.html",
	"/jp/about/index.html", "/jp/achievements/index.html", "/jp/computers/index.html",
	"/jp/contact/index.html", "/jp/index.html", "/jp/links/index.html", "/jp/member/index.html",
	"/jp/member/yokota.html", "/jp/news/index.html", "/jp/picture/index.html",
	"/jp/research/index.html", "/jp/software/index.html", "/jp/teaching/index.html"
];

test("all routes and local interactive components run without browser errors", async ({ browser }) => {
	test.setTimeout(90000);
	const failures = [];
	for (const width of [320, 1200]) {
		const context = await browser.newContext({
			baseURL: "http://127.0.0.1:8765", viewport: { width, height: 800 }
		});
		await context.addInitScript(([key, value]) => localStorage.setItem(key, value), [storageKey, "rejected"]);
		const page = await context.newPage();
		let route = "startup";
		page.on("pageerror", error => failures.push(`${width}px ${route}: exception: ${error.message}`));
		page.on("console", message => {
			if (message.type() === "error") failures.push(`${width}px ${route}: console: ${message.text()}`);
		});
		page.on("requestfailed", request => {
			if (new URL(request.url()).origin === "http://127.0.0.1:8765") {
				failures.push(`${width}px ${route}: request failed: ${request.url()} (${request.failure()?.errorText})`);
			}
		});
		page.on("response", response => {
			if (new URL(response.url()).origin === "http://127.0.0.1:8765" && response.status() >= 400) {
				failures.push(`${width}px ${route}: HTTP ${response.status()}: ${response.url()}`);
			}
		});
		for (route of routes) {
			await page.goto(route, { waitUntil: "load" });
			if (width === 320) {
				const button = page.locator("#menubar_hdr");
				await button.click();
				await expect(page.locator("#menubar-s")).toBeVisible();
				await button.click();
			}
			if (await page.locator("[data-lightbox]").count()) {
				await page.locator("[data-lightbox]").first().click();
				await expect(page.locator("#lightbox")).toBeVisible();
				await expect(page.locator(".lb-close")).toBeFocused();
				await page.keyboard.press("Escape");
				await expect(page.locator("#lightbox")).toBeHidden();
			}
			await page.waitForTimeout(25);
		}
		await context.close();
	}
	expect(failures, failures.join("\n")).toEqual([]);
});
