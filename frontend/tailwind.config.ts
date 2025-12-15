import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Cores primárias do site original
        primary: '#d62042',
        'primary-light': '#ff6b6b',
        'primary-dark': '#a71e56',
        secondary: '#007bff',
        accent: '#00d084',
        
        // Backgrounds
        dark: '#0c0d0e',
        'dark-2': '#110e0e',
        'dark-3': '#1f2124',
        background: '#000000',
        
        // Borders e overlays
        border: 'rgba(255,255,255,0.12)',
        'border-light': 'rgba(255,255,255,0.24)',
        tint: 'rgba(214,32,66,0.18)',
        overlay: 'rgba(0,0,0,0.8)',
        
        // Text
        text: '#ffffff',
        'text-muted': '#e9ecef',
        'text-gray': '#6c757d',
        
        // States
        success: '#28a745',
        warning: '#fcb900',
        danger: '#cf2e2e',
        info: '#0693e3',
      },
      fontFamily: {
        base: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        heading: ['Poppins', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      fontSize: {
        xs: 'clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)',
        sm: 'clamp(0.875rem, 0.8rem + 0.375vw, 1rem)',
        base: 'clamp(1rem, 0.9rem + 0.5vw, 1.125rem)',
        lg: 'clamp(1.125rem, 1rem + 0.625vw, 1.25rem)',
        xl: 'clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem)',
        '2xl': 'clamp(1.5rem, 1.3rem + 1vw, 2rem)',
        '3xl': 'clamp(1.875rem, 1.6rem + 1.375vw, 2.5rem)',
        '4xl': 'clamp(2.25rem, 1.9rem + 1.75vw, 3rem)',
        '5xl': 'clamp(3rem, 2.5rem + 2.5vw, 4rem)',
      },
      borderRadius: {
        'lg': '12px',
        'xl': '18px',
        '2xl': '24px',
        'full': '9999px',
      },
      boxShadow: {
        'kaizen': '0 12px 40px rgba(0,0,0,.35)',
        'kaizen-lg': '0 18px 50px rgba(214,32,66,.18)',
      },
    },
  },
  plugins: [],
}
export default config



