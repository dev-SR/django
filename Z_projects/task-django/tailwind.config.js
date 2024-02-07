/** @type {import('tailwindcss').Config} */
module.exports = {
	darkMode: 'class',

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
		extend: {},
		fontFamily: {
			sans: ['Inter', 'sans-serif']
		}
	},
	plugins: [require('@tailwindcss/forms')]
};
