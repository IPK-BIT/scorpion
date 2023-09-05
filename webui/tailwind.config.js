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
					"primary": "#33691b",
					"secondary": "#7af842",
					"accent": "#00f7fb",
					"neutral": "#b2b2b2",
					"base-100": "#e7fddd",
					"info": "#3ABFF8",
					"success": "#36D399",
					"warning": "#FBBD23",
					"error": "#F87272",
				},
			}
		],
	},
  plugins: [require("daisyui")],
}

