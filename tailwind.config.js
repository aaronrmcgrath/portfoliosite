/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      fontFamily: {
        'mono': ['IBM Plex Mono', 'Courier New', 'monospace'],
        'brutal': ['Inter', 'Helvetica Neue', 'sans-serif'],
        'serif': ['Playfair Display', 'Georgia', 'Times New Roman', 'serif'],
        'newspaper': ['Source Serif Pro', 'Georgia', 'serif'],
      },
      colors: {
        'terminal': {
          'green': '#00ff00',
          'amber': '#ffb000',
          'bg': '#0a0a0a',
        },
        'newsprint': {
          'cream': '#f5f2e8',
          'ink': '#1a1a1a',
          'rule': '#8b8b8b',
        },
      },
    },
  },
  plugins: [],
}
