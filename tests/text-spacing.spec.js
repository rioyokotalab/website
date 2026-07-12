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
const override = `
	* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; }
	p { margin-bottom: 2em !important; }
`;

test("user text-spacing overrides do not clip or create page overflow", async ({ browser }) => {
	test.setTimeout(90000);
	const failures = [];
	for (const width of [320, 1200]) {
		const context = await browser.newContext({
			baseURL: "http://127.0.0.1:8765", viewport: { width, height: 800 }
		});
		await context.addInitScript(([key, value]) => localStorage.setItem(key, value), [storageKey, "rejected"]);
		const page = await context.newPage();
		for (const route of routes) {
			await page.goto(route, { waitUntil: "domcontentloaded" });
			await page.addStyleTag({ content: override });
			await page.evaluate(() => window.dispatchEvent(new Event("resize")));
			if (width === 320) {
				await page.locator("#menubar_hdr").click();
				await expect(page.locator("#menubar-s")).toBeVisible();
			}
			const result = await page.evaluate(viewportWidth => ({
				documentWidth: document.documentElement.scrollWidth,
				clipped: [...document.querySelectorAll("body *")].filter(element => {
					const style = getComputedStyle(element);
					const rectangle = element.getBoundingClientRect();
					if (!element.textContent.trim() || rectangle.width <= 0 || rectangle.height <= 0) return false;
					const descendants = [...element.querySelectorAll("*")].filter(child => {
						const childRectangle = child.getBoundingClientRect();
						return child.textContent.trim() && childRectangle.width > 0 && childRectangle.height > 0 &&
							getComputedStyle(child).visibility !== "hidden";
					});
					const hasScroller = (child, axis) => {
						for (let ancestor = child.parentElement; ancestor && ancestor !== element; ancestor = ancestor.parentElement) {
							const overflow = getComputedStyle(ancestor)[axis];
							if (overflow === "auto" || overflow === "scroll") return true;
						}
						return false;
					};
					const clipsX = style.overflowX === "hidden" && descendants.some(child => {
						const childRectangle = child.getBoundingClientRect();
						return !hasScroller(child, "overflowX") && (childRectangle.left < rectangle.left - 1 || childRectangle.right > rectangle.right + 1);
					});
					const clipsY = style.overflowY === "hidden" && descendants.some(child => {
						const childRectangle = child.getBoundingClientRect();
						return !hasScroller(child, "overflowY") && (childRectangle.top < rectangle.top - 1 || childRectangle.bottom > rectangle.bottom + 1);
					});
					return clipsX || clipsY;
				}).map(element => `${element.tagName}${element.id ? `#${element.id}` : ""}${element.className && typeof element.className === "string" ? `.${element.className.trim().replace(/\s+/g, ".")}` : ""}`),
				unusableScrollers: [...document.querySelectorAll(".mobile-table-containment table")].filter(table =>
					table.scrollWidth > table.clientWidth + 1 && table.getAttribute("tabindex") !== "0").length,
				fixedOutside: [...document.querySelectorAll("button, [tabindex], .analytics-consent-settings")].filter(element => {
					if (getComputedStyle(element).position !== "fixed" || getComputedStyle(element).display === "none") return false;
					const rectangle = element.getBoundingClientRect();
					return rectangle.left < -0.5 || rectangle.right > viewportWidth + 0.5;
				}).map(element => element.id || element.className)
			}), width);
			if (result.documentWidth > width) failures.push(`${width}px ${route}: document width ${result.documentWidth}`);
			for (const element of result.clipped) failures.push(`${width}px ${route}: clipped ${element}`);
			if (result.unusableScrollers) failures.push(`${width}px ${route}: ${result.unusableScrollers} unfocusable table scrollers`);
			for (const element of result.fixedOutside) failures.push(`${width}px ${route}: fixed control outside ${element}`);
		}
		await context.close();
	}
	expect(failures, failures.join("\n")).toEqual([]);
});

test("fresh EN/JP consent controls remain usable with expanded text spacing", async ({ page }) => {
	await page.setViewportSize({ width: 320, height: 800 });
	for (const route of ["/en/index.html", "/jp/index.html"]) {
		await page.goto(route);
		await page.evaluate(key => localStorage.removeItem(key), storageKey);
		await page.reload();
		await page.addStyleTag({ content: override });
		const consent = page.locator("#analytics-consent");
		await expect(consent).toBeVisible();
		expect(await consent.evaluate(element => element.getBoundingClientRect().width)).toBeLessThanOrEqual(320);
		for (const button of await consent.locator("button").all()) await expect(button).toBeVisible();
	}
});
