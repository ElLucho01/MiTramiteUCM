const { defineConfig } = require("cypress")

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://backend:5000",
    reporter: "json",
    reporterOptions: {
      outputFile: "cypress/reports/report.json",
    },
  }
})


