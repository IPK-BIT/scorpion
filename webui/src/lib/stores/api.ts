import { readable, writable, type Readable, type Writable } from 'svelte/store';
import type { API, License, ServiceOverview, Token } from './types';

export const api: Readable<API> = readable({
	base_url: 'https://scorpion.bi.denbi.de',
	modules: {
		aai: '/aai',
		v1: '/api/v1'
	}
});

export const token: Writable<Token> = writable('');

export const serviceOverview: Writable<ServiceOverview> = writable({
	categories: [],
	providers: [],
	licenses: []
});

export const licenses: Writable<License[]> = writable([]);
