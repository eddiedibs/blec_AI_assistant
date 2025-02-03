const colors = require('tailwindcss/colors')
const flowbite = require("flowbite-react/tailwind");


module.exports = {
  // resolve: {
  //   alias: {
  //     'flowbite': path.resolve(__dirname, 'node_modules/flowbite'),
  //   },
  // },
  content: [
    "./node_modules/flowbite-react/**/*.js", 
    "./src/**/*.{js,jsx,ts,tsx}",
    flowbite.content(),
  ],
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
        primary: '#9d2a92',
        secondary: '#3fae48',
        purple: colors.truePurple,
        purple: {
          900: '#9d2a92',
        },
        magenta: '#FF96D8',
        greenKid: {
          500: '#39a142',
          900: '#3fae48',
        }
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    flowbite.plugin(),
    require('flowbite/plugin'),
  ],
}
