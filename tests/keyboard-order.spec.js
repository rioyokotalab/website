const { test, expect } = require("@playwright/test");

const storageKey = "yokota_analytics_consent_v1";
const routes = [
	"about/index.html", "achievements/index.html", "computers/index.html", "contact/index.html",
	"index.html", "links/index.html", "member/index.html", "member/yokota.html", "news/index.html",
	"picture/index.html", "research/index.html", "software/index.html", "teaching/index.html"
];

test.setTimeout(180_000);

test("every route has a complete, duplicate-free keyboard sequence", async ({ browser }) => {
	for (const width of [390, 1200]) {
		const context = await browser.newContext({ viewport: { width, height: 800 } });
		await context.addInitScript(([key, value]) => localStorage.setItem(key, value), [storageKey, "rejected"]);
		const page = await context.newPage();
		for (const language of ["en", "jp"]) {
			for (const route of routes) {
				await page.goto(`/${language}/${route}`, { waitUntil: "domcontentloaded" });
				await expect(page.locator("#analytics-consent-settings")).toBeVisible();
				const expected = await page.locator("a[href], button:not([disabled]), iframe, [tabindex]:not([tabindex='-1'])").evaluateAll(elements =>
				elements.filter(element => {
					const style = getComputedStyle(element);
					const rect = element.getBoundingClientRect();
					if (style.display === "none" || style.visibility === "hidden" || rect.width <= 0 || rect.height <= 0) return false;
					for (let ancestor = element.parentElement; ancestor; ancestor = ancestor.parentElement) {
						const ancestorStyle = getComputedStyle(ancestor);
						if (ancestorStyle.display === "none" || ancestorStyle.visibility === "hidden") return false;
						if ([ancestorStyle.overflow, ancestorStyle.overflowX, ancestorStyle.overflowY].some(value => value === "hidden" || value === "clip")) {
							const clip = ancestor.getBoundingClientRect();
							if (rect.right <= clip.left || rect.left >= clip.right || rect.bottom <= clip.top || rect.top >= clip.bottom) return false;
						}
					}
					return true;
				}).map((element, index) => {
					const id = `keyboard-target-${index}`;
					element.dataset.keyboardTarget = id;
					return `${id}:${element.tagName}:${element.id || element.getAttribute("href") || ""}`;
				}));
				const visited = [];
				await page.locator("body").focus();
				for (let index = 0; index < expected.length; index += 1) {
					await page.keyboard.press("Tab");
					visited.push(await page.evaluate(() => {
						const element = document.activeElement;
						return `${element?.dataset.keyboardTarget || ""}:${element?.tagName || ""}:${element?.id || element?.getAttribute?.("href") || ""}`;
					}));
				}
				expect(visited, `${language}/${route} at ${width}px`).toEqual(expected);
				await page.keyboard.press("Shift+Tab");
				expect(await page.evaluate(() => {
					const element = document.activeElement;
					return `${element?.dataset.keyboardTarget || ""}:${element?.tagName || ""}:${element?.id || element?.getAttribute?.("href") || ""}`;
				})).toBe(expected.at(-2));
			}
		}
		await context.close();
	}
});
