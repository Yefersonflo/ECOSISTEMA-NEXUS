/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html"
  ],
  theme: {
    extend: {
      colors: {
        'comfablue': '#1B51A2',
        'comfayellow': '#FFD101',
        'comfared': '#F05623'
      }
    },
  },
  plugins: [],
}
