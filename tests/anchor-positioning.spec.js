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

test("same-page heading links stay below sticky navigation", async ({ browser }) => {
	test.setTimeout(90000);
	let checked = 0;
	for (const width of [320, 900, 901, 1200]) {
		const context = await browser.newContext({
			baseURL: "http://127.0.0.1:8765", reducedMotion: "reduce", viewport: { width, height: 800 }
		});
		await context.addInitScript(([key, value]) => localStorage.setItem(key, value), [storageKey, "rejected"]);
		const page = await context.newPage();
		for (const route of routes) {
			await page.goto(route, { waitUntil: "domcontentloaded" });
			const links = page.locator('a[href^="#"]');
			for (let index = 0; index < await links.count(); index += 1) {
				const link = links.nth(index);
				const hash = await link.getAttribute("href");
				if (!hash || hash === "#") continue;
				const isHeading = await page.locator(hash).evaluateAll(elements =>
					elements.length === 1 && elements[0].matches("h3.heading[id]"));
				if (!isHeading) continue;
				await link.evaluate(element => element.click());
				const geometry = await page.locator(hash).evaluate(element => {
					const target = element.getBoundingClientRect();
					const navigation = document.getElementById("navbar").getBoundingClientRect();
					return { top: target.top, bottom: target.bottom, navigationBottom: Math.max(0, navigation.bottom) };
				});
				expect(geometry.top, `${route} ${hash} at ${width}px`).toBeGreaterThanOrEqual(geometry.navigationBottom + 1);
				expect(geometry.bottom, `${route} ${hash} at ${width}px`).toBeLessThanOrEqual(800);
				checked += 1;
			}
		}
		await context.close();
	}
	expect(checked).toBeGreaterThan(100);
});
