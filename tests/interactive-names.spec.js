const { test, expect } = require("@playwright/test");

const storageKey = "yokota_analytics_consent_v1";
const routes = [
	"about/index.html", "achievements/index.html", "computers/index.html", "contact/index.html",
	"index.html", "links/index.html", "member/index.html", "member/yokota.html", "news/index.html",
	"picture/index.html", "research/index.html", "software/index.html", "teaching/index.html"
];

test("every rendered interactive has a nonempty accessible name", async ({ browser }) => {
	const context = await browser.newContext({ viewport: { width: 1200, height: 800 } });
	await context.addInitScript(([key, value]) => localStorage.setItem(key, value), [storageKey, "rejected"]);
	const page = await context.newPage();
	for (const language of ["en", "jp"]) {
		for (const route of routes) {
			await page.goto(`/${language}/${route}`, { waitUntil: "domcontentloaded" });
			await expect(page.locator("#analytics-consent-settings")).toBeVisible();
			for (const role of ["link", "button"]) {
				for (const interactive of await page.getByRole(role).all()) {
					const firstLine = (await interactive.ariaSnapshot()).split("\n", 1)[0];
					expect(firstLine, `${language}/${route}: ${firstLine}`).toMatch(new RegExp(`^- ['"]?${role} ".+"`));
				}
			}
			for (const frame of await page.locator("iframe").all()) {
				expect((await frame.getAttribute("title") || "").trim().length).toBeGreaterThan(0);
			}
		}
	}
	await context.close();
});
