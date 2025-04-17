
import { readable, writable } from 'svelte/store';


export const api = readable({
	base_url: 'https://scorpion.bi.denbi.de',
	modules: {
		aai: '/aai',
		v1: '/api/v1'
	}
});

export const token = writable('');

export const serviceOverview = writable({
	categories: [],
	providers: [],
	licenses: []
});

export const licenses = writable([]);
