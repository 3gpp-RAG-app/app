/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      'white': '#ffffff',
      'midnight_blue': '#161238',
      'sapphire_blue': '#28388d',
      'periwinkle_blue': '#7387c2',
      'powder_blue': '#c6d4fb',
      'lavender': '#bcacdb'
    },
  },
  plugins: [],
}

