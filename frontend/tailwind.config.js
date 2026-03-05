/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        'figma-yellow': '#fef08a', // Le jaune des boutons "SIGN IN" et "GET STARTED"
        'figma-bg': '#ffffff',     // Le fond principal blanc
        'figma-gray-light': '#f3f4f6', // Le gris clair des zones de contenu
        'figma-gray-card': '#e5e7eb',  // Le gris des placeholders d'images
        'figma-text': '#1f2937'    // Le texte foncé
      }
    },
  },
  plugins: [],
}