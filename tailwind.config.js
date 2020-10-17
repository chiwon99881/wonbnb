// if you modify this file, you must run this command : "num run css"
// for customized: refer to https://tailwindcss.com/docs/border-radius#customizing
module.exports = {
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
    // defaultLineHeights: true,
    // standardFontWeights: true
  },
  purge: [],
  theme: {
    extend: {
      spacing: {
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh"
      },
      borderRadius: {
        circle: "50%"
      }
    }
  },
  variants: {},
  plugins: []
}
