/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {},
	},
	daisyui: {
		themes: [
			{
				mytheme: {
					"primary": "#011126",
					"secondary": "#00070D",
					"accent": "#A4B3BF",
					"neutral": "#011826",
					"base-100": "#F0F2F2",
					"info": "#0A2062",
					"success": "#006730",
					"warning": "#9E8905",	
					"error": "#911707",
				},
			}
		],
	},
	plugins: [require("daisyui")],
}

