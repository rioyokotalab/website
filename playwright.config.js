const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
	testDir: "./tests",
	fullyParallel: false,
	workers: 1,
	retries: 0,
	reporter: "line",
	outputDir: ".playwright/test-results",
	use: {
		baseURL: "http://127.0.0.1:8765",
		headless: true,
		serviceWorkers: "block",
		trace: "retain-on-failure"
	},
	webServer: {
		command: "python3 tools/quiet-http-server.py 8765 --bind 127.0.0.1",
		url: "http://127.0.0.1:8765/en/index.html",
		reuseExistingServer: false,
		timeout: 10000
	}
});
