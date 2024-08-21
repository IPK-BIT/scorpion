import { readable, writable, type Readable, type Writable } from 'svelte/store';
import type { API, License, ServiceOverview, Token } from './types';
// @ts-ignore
import {PUBLIC_API_URL} from '$env/static/public';

export const api: Readable<API> = readable({
	base_url: PUBLIC_API_URL,
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
