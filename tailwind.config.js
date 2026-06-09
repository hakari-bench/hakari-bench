/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./hakari_bench/viewer/**/*.py",
    "./hakari_bench/viewer/assets/viewer.js",
    "./tests/test_viewer*.py",
  ],
  safelist: ["htmx-request"],
  theme: {
    extend: {},
  },
  plugins: [],
};
