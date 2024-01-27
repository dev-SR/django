/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		// Templates within theme app (e.g. base.html)
		'./templates/**/*.html',
		// Templates in other apps
		'./../templates/**/*.html'
		// // Include JavaScript files that might contain Tailwind CSS classes
		// '../../**/*.js',
		// // Include Python files that might contain Tailwind CSS classes
		// '../../**/*.py'
	],
	theme: {
		extend: {}
	},
	daisyui: {
		themes: [
			'light' // first one will be the default theme
		]
	},
	plugins: [require('@tailwindcss/forms'), require('daisyui')]
};
