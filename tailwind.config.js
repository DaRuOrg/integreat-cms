const colors = require('tailwindcss/colors')

module.exports = {
  content: [
    './integreat_cms/cms/templates/**/*.html',
    './integreat_cms/static/src/js/**/*.{js,ts,tsx}',
  ],
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      black: colors.black,
      white: colors.white,
      gray: colors.slate,
      red: colors.red,
      orange: colors.orange,
      yellow: colors.yellow,
      green: colors.green,
      blue: colors.blue,
    },
    extend: {
      colors: {
        // generated from #fbda16 with https://javisperez.github.io/tailwindcolorshades/
        'integreat': {
          '50': '#fffdf3',
          '100': '#fffbe8',
          '200': '#fef6c5',
          '300': '#fdf0a2',
          '400': '#fce55c',
          '500': '#fbda16',
          '600': '#e2c414',
          '700': '#bca411',
          '800': '#97830d',
          '900': '#7b6b0b'
        },
        'water': {
          '50': '#fefeff', 
          '100': '#fcfdff', 
          '200': '#f8fafe', 
          '300': '#f4f7fe', 
          '400': '#ecf1fd', 
          '500': '#e4ebfc', 
          '600': '#cdd4e3', 
          '700': '#abb0bd', 
          '800': '#898d97', 
          '900': '#70737b'
        }
      },
      backgroundImage: {
        'icon': "url('../images/integreat-icon.png')",
        'logo': "url('../images/integreat-logo.png')",
        'logo-white': "url('../images/integreat-logo-white.png')",
        'logo-yellow': "url('../images/integreat-logo-yellow.png')",
        'border-left': 'linear-gradient(to right, var(--tw-gradient-from), var(--tw-gradient-from) 4px, var(--tw-gradient-to, rgba(0, 0, 0, 0)) 4px)',
      },
      fontFamily: {
        'default': ["Raleway", "Lateef", "Noto Sans SC", "sans-serif"],
        'content': ["Open Sans", "sans-serif"],
        'content-rtl': ["Lateef", "sans-serif"],
        'content-sc': ["Noto Sans SC", "sans-serif"],
      },
      maxHeight: {
        '15': '3.75rem',
        '116': '29rem',
        '160': '40rem',
      },
      gridTemplateColumns: {
        'gallery': 'repeat(auto-fill, minmax(180px, 1fr))',
      },
      width: {
        '120': '30rem',
        '136': '34rem',
      },
      screens: {
        '3xl': '1700px',
        '4xl': '2100px',
      },
    },
  },
  plugins: [require('@tailwindcss/forms'),],
}