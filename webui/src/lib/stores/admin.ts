import { readable, writable, type Readable, type Writable } from 'svelte/store';
import type {
	KPI,
	MembershipRequest,
	Necessity,
	RegistrationRequest,
	ServiceCategory,
	ServiceProvider,
	UserDetail
} from './types';

export const categories: Writable<ServiceCategory[]> = writable([]);
export const providers: Writable<ServiceProvider[]> = writable([]);
export const indicators: Writable<KPI[]> = writable([]);

export const open_requests: Writable<MembershipRequest[]> = writable([]);
export const users: Writable<UserDetail[]> = writable([]);
export const registration_requests: Writable<RegistrationRequest[]> = writable([]);

export const necessities: Readable<Necessity[]> = readable([
	'mandatory',
	'recommended',
	'optional'
]);
