import { readable, writable, type Writable } from 'svelte/store';
import type { KPI, MeasurementCollector } from './types';

export const steps = readable([
	{
		title: 'Overarching Information about a Consortium',
		shortTitle: 'Data Sheet 1',
		components: [
			{
				type: 'datasheet1',
				config: {}
			}
		]
	},
	{
		title: "Information about a Consortium's Networking with the Community",
		shortTitle: 'Data Sheet 2',
		components: [
			{
				type: 'datasheet2',
				config: {}
			}
		]
	},
	{
		title: 'Overview of the Research Data of a Consortium',
		shortTitle: 'Data Sheet 3',
		components: [
			{
				type: 'datasheet3',
				config: {}
			}
		]
	},
	{
		title: 'Overview of the Services of a Consortium',
		shortTitle: 'Data Sheet 4',
		components: [
			{
				type: 'datasheet4',
				config: {}
			}
		]
	}
	// {
	//     title: 'Information about each Individual Service of a Consortium',
	//     shortTitle: 'Data Sheet 5',
	//     components: [
	//         {
	//             type: 'datasheet5',
	//             config: {}
	//         }
	//     ]
	// }
]);

export const indicators: Writable<KPI[]> = writable([]);

export const measurements: Writable<MeasurementCollector> = writable({});
