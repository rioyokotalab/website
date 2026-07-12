const { test, expect } = require("@playwright/test");

const routes = [
	"about/index.html", "achievements/index.html", "computers/index.html", "contact/index.html",
	"index.html", "links/index.html", "member/index.html", "member/yokota.html", "news/index.html",
	"picture/index.html", "research/index.html", "software/index.html", "teaching/index.html"
];

test("every route preserves localized structural and responsive navigation landmarks", async ({ browser }) => {
	for (const width of [390, 1200]) {
		const context = await browser.newContext({ viewport: { width, height: 800 } });
		const page = await context.newPage();
		for (const language of ["en", "jp"]) {
			for (const route of routes) {
				await page.goto(`/${language}/${route}`, { waitUntil: "domcontentloaded" });
				await expect(page.getByRole("banner")).toHaveCount(1);
				await expect(page.getByRole("main")).toHaveCount(1);
				await expect(page.getByRole("contentinfo")).toHaveCount(1);
				if (width === 1200) {
					const name = language === "en" ? "Primary navigation" : "メインナビゲーション";
					await expect(page.getByRole("navigation", { name, exact: true })).toHaveCount(1);
					await expect(page.getByRole("navigation")).toHaveCount(1);
				} else {
					await expect(page.getByRole("navigation")).toHaveCount(0);
					await page.locator("#menubar_hdr").click();
					const name = language === "en" ? "Mobile navigation" : "モバイルナビゲーション";
					await expect(page.getByRole("navigation", { name, exact: true })).toHaveCount(1);
					await expect(page.getByRole("navigation")).toHaveCount(1);
				}
			}
		}
		await context.close();
	}
});
