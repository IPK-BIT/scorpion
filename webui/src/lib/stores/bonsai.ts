import { readable, writable } from 'svelte/store';

export const steps = readable([
	{
		title: 'General Information',
		shortTitle: 'General',
		components: [
			{
				type: 'general',
				config: {}
			}
		]
	},
	{
		title: 'Reporting Information',
		shortTitle: 'Reporting',
		components: [
			{
				type: 'reporting',
				config: {}
			}
		]
	}
]);

export const metadata = writable({
	name: '',
	abbreviation: '',
	provider: '',
	consortia: [],
	license: '',
	stage: '',
	category: '',
	additionalKPI: []
});

export function reset() {
	metadata.set({
		name: '',
		abbreviation: '',
		provider: '',
		consortia: [],
		license: '',
		stage: '',
		category: '',
		additionalKPI: []
	});
}
