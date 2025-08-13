/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['"Plus Jakarta Sans"', '"Noto Sans"', 'sans-serif'],
      },
      colors: {
        'primary': '#2071f3',
        'background': '#f8f9fc',
        'text-primary': '#0d131c',
        'text-secondary': '#49699c',
        'input-bg': '#e7ecf4',
      },
    },
  },
  plugins: [],
}