module.exports = {
	content: ['templates/**/*.html', './**/templates/**/*.html'],
	darkMode: 'class', // or 'media' or 'class'
	theme: {
		extend: {}
	},
	variants: {
		extend: {}
	},
	plugins: [require('@tailwindcss/forms')]
};
