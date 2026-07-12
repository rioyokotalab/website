const { test, expect } = require("@playwright/test");

const storageKey = "yokota_analytics_consent_v1";
const googleRequest = /(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com)/;

async function observeGoogle(page) {
	const requests = [];
	page.on("request", request => {
		if (googleRequest.test(request.url())) {
			requests.push(request.url());
		}
	});
	await page.route(googleRequest, route => {
		if (route.request().url().includes("googletagmanager.com/gtag/js")) {
			return route.fulfill({
				status: 200,
				contentType: "application/javascript",
				body: "window.__mockGoogleTagLoaded = true;"
			});
		}
		return route.abort("blockedbyclient");
	});
	return requests;
}

test("English fresh visit and rejection send no Google request", async ({ browser }) => {
	const context = await browser.newContext();
	const page = await context.newPage();
	const requests = await observeGoogle(page);

	await page.goto("/en/index.html");
	const banner = page.locator("#analytics-consent");
	await expect(banner).toBeVisible();
	await expect(banner).toHaveAttribute("aria-label", "Analytics consent settings");
	await expect(banner.locator("h2")).toHaveText("Analytics and privacy");
	await expect(page.locator(".analytics-consent-reject")).toBeFocused();
	expect(requests).toEqual([]);

	await page.locator(".analytics-consent-reject").click();
	await expect(banner).toHaveCount(0);
	await expect(page.locator("#analytics-consent-settings")).toBeVisible();
	expect(await page.evaluate(key => localStorage.getItem(key), storageKey)).toBe("rejected");
	expect(requests).toEqual([]);

	await page.reload();
	await expect(page.locator("#analytics-consent")).toHaveCount(0);
	await expect(page.locator("#analytics-consent-settings")).toBeVisible();
	expect(requests).toEqual([]);
	await context.close();
});

test("keyboard settings and acceptance persist with privacy-first consent values", async ({ browser }) => {
	const context = await browser.newContext();
	const page = await context.newPage();
	const requests = await observeGoogle(page);

	await page.goto("/en/index.html");
	await page.locator(".analytics-consent-reject").click();
	await page.locator("#analytics-consent-settings").focus();
	await page.keyboard.press("Enter");
	await expect(page.locator(".analytics-consent-reject")).toBeFocused();
	await page.keyboard.press("Tab");
	await expect(page.locator(".analytics-consent-accept")).toBeFocused();
	await page.keyboard.press("Enter");

	await expect.poll(() => requests.length).toBe(1);
	expect(requests[0]).toContain("id=G-DVRGG7FDLX");
	expect(await page.evaluate(key => localStorage.getItem(key), storageKey)).toBe("accepted");
	const consentQueue = await page.evaluate(() => dataLayer.map(entry => Array.from(entry)));
	expect(consentQueue).toHaveLength(4);
	expect(consentQueue[0]).toEqual(["consent", "default", {
		ad_storage: "denied",
		ad_user_data: "denied",
		ad_personalization: "denied",
		analytics_storage: "denied"
	}]);
	expect(consentQueue[1]).toEqual(["consent", "update", {
		ad_storage: "denied",
		ad_user_data: "denied",
		ad_personalization: "denied",
		analytics_storage: "granted"
	}]);

	await page.reload();
	await expect.poll(() => requests.length).toBe(2);
	await expect(page.locator("#analytics-consent")).toHaveCount(0);
	await expect(page.locator("#analytics-consent-settings")).toBeVisible();
	await context.close();
});

test("revocation removes GA cookies and reloads without another Google request", async ({ browser }) => {
	const context = await browser.newContext();
	const page = await context.newPage();
	const requests = await observeGoogle(page);

	await page.goto("/en/index.html");
	await page.locator(".analytics-consent-accept").click();
	await expect.poll(() => requests.length).toBe(1);
	await context.addCookies([
		{ name: "_ga", value: "test", url: "http://127.0.0.1:8765" },
		{ name: "_ga_TEST", value: "test", url: "http://127.0.0.1:8765" }
	]);

	await page.locator("#analytics-consent-settings").click();
	await Promise.all([
		page.waitForNavigation(),
		page.locator(".analytics-consent-reject").click()
	]);
	await expect(page.locator("#analytics-consent-settings")).toBeVisible();
	expect(await page.evaluate(key => localStorage.getItem(key), storageKey)).toBe("rejected");
	expect(requests).toHaveLength(1);
	const cookies = await context.cookies();
	expect(cookies.filter(cookie => cookie.name === "_ga" || cookie.name.startsWith("_ga_"))).toEqual([]);
	await context.close();
});

test("Japanese mobile banner is translated, stacked, and does not overflow", async ({ browser }) => {
	const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
	const page = await context.newPage();
	const requests = await observeGoogle(page);

	await page.goto("/jp/index.html");
	const banner = page.locator("#analytics-consent");
	await expect(banner).toBeVisible();
	await expect(banner).toHaveAttribute("aria-label", "アクセス解析の同意設定");
	await expect(banner.locator("h2")).toHaveText("アクセス解析について");
	await expect(page.locator(".analytics-consent-accept")).toHaveText("同意する");
	await expect(page.locator(".analytics-consent-reject")).toHaveText("同意しない");
	expect(await banner.evaluate(element => getComputedStyle(element).flexDirection)).toBe("column");
	expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
	expect(requests).toEqual([]);
	await context.close();
});
