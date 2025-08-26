/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./templates/**/*.html",
      "./contacts/templates/**/*.html",
      "./contacts/static/**/*.js",
    ],
    theme: {
      extend: {},
    },
    plugins: [require("daisyui")],
  };