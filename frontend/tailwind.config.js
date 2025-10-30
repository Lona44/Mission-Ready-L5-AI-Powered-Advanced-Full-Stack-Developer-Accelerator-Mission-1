/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'turners-blue': '#003087',
        'turners-red': '#E31E24',
      }
    },
  },
  plugins: [],
}
