const colors = require('tailwindcss/colors')


module.exports = {
  mode: 'jit',
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        primary: '#B571FF',
        secondary: '#FF96D8',
        purple: colors.truePurple,
        purple: {
          900: '#B571FF',
        },
        magenta: '#FF96D8'
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
