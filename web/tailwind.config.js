/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    "./assets/**/*.{css,js}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#f97316",
          50: "#fff7ed",
          100: "#ffedd5",
          200: "#fed7aa",
          300: "#fdba74",
          400: "#fb923c",
          500: "#f97316",
          600: "#ea580c",
          700: "#c2410c",
          800: "#9a3412",
          900: "#7c2d12",
        },
      },
      fontFamily: {
        display: ["Oxanium", "ui-sans-serif", "system-ui", "sans-serif"],
        sans: ["Sarabun", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      container: {
        center: true,
        padding: "1rem",
        screens: { md: "720px", lg: "960px", xl: "1140px", "2xl": "1320px" },
      },
      boxShadow: {
        soft: "0 5px 20px rgba(15, 92, 250, .08)",
        glow: "0 0 0 1px rgba(249,115,22,.15), 0 20px 60px rgba(249,115,22,.15)",
      },
      backgroundImage: {
        grain: "url('/static/img/grain.png')",
        diag: "linear-gradient(135deg, rgba(255,255,255,.06) 0%, rgba(255,255,255,.01) 100%)",
      },
      borderRadius: { xl2: "1.25rem" },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
