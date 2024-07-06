const colors = require('tailwindcss/colors')


module.exports = {
  mode: 'jit',
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    screens: {
      sm: '640px', // default
      md: '768px', // default
      lg: '1024px', // default
      xl: '1280px', // default
      '2xl': '1536px', // default
      '3xl': '1920px', // custom breakpoint
    },
    extend: {
      fontFamily: {
        montserrat: ['Montserrat', 'sans-serif'], // Replace 'YourFontName' with the actual name of your font
      },
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
