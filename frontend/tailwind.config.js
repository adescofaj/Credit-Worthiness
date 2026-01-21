/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'deep-coffee': '#4B2E05',
        'medium-brown': '#7B4B2A',
        'light-tan': '#CBB193',
        'cream-bg': '#F5EDE0',
        'off-white': '#FFF9F4',
        'muted-gold': '#D4A373',
        'text-dark': '#3C2A21',
      },
    },
  },
  plugins: [],
}