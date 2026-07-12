const { test, expect } = require("@playwright/test");

const routes = [
	"about/index.html", "achievements/index.html", "computers/index.html", "contact/index.html",
	"index.html", "links/index.html", "member/index.html", "member/yokota.html", "news/index.html",
	"picture/index.html", "research/index.html", "software/index.html", "teaching/index.html"
];

test("every EN/JP route exposes one meaningful level-one heading", async ({ page }) => {
	for (const language of ["en", "jp"]) {
		for (const route of routes) {
			await page.goto(`/${language}/${route}`, { waitUntil: "domcontentloaded" });
			const levelOne = page.getByRole("heading", { level: 1 });
			await expect(levelOne).toHaveCount(1);
			expect((await levelOne.textContent()).trim().length).toBeGreaterThan(0);
			expect(await levelOne.getAttribute("class")).toBe("visually-hidden");
		}
	}
});
