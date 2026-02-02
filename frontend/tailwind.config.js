/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // Colores EMI Institucionales
                emi: {
                    navy: {
                        50: '#e6eaf0',
                        100: '#ccd5e1',
                        200: '#99abc3',
                        300: '#6680a5',
                        400: '#335687',
                        500: '#003366', // Principal
                        600: '#002952',
                        700: '#001f3d',
                        800: '#001529',
                        900: '#000a14',
                    },
                    gold: {
                        50: '#faf6e8',
                        100: '#f5edd1',
                        200: '#ebdba3',
                        300: '#e1c975',
                        400: '#d7b747',
                        500: '#D4AF37', // Principal
                        600: '#C5B358', // Alternativo
                        700: '#8a7a26',
                        800: '#5c5119',
                        900: '#2e290d',
                    }
                },
                // Estados semanticos
                success: {
                    light: '#D4AF37', // Dorado EMI para exito
                    DEFAULT: '#C5B358',
                    dark: '#8a7a26',
                },
                danger: {
                    light: '#fee2e2',
                    DEFAULT: '#DC3545',
                    dark: '#991b1b',
                }
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
