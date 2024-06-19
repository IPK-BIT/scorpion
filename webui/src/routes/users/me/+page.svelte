<script lang="ts">
	import Profile from '$lib/components/profile/Profile.svelte';
	import { api } from '$lib/stores/api';
	import type { MembershipRequest, ServiceProvider, UserDetail } from '$lib/stores/types';
	import axios from 'axios';
	import { onMount } from 'svelte';

	let details: UserDetail = { user_name: '', email: '', is_admin: false, providers: [] };
	let providers: ServiceProvider[] = [];
	let openRequests: MembershipRequest[] = [];
	onMount(async () => {
		let response = await axios.get('/details', {
			baseURL: $api.base_url + $api.modules.aai
		});
		if (response.status === 200) {
			details = response.data;
		}
		response = await axios.get('/providers', {
			baseURL: $api.base_url + $api.modules.v1
		});
		providers = response.data.result
			.filter((e: ServiceProvider) => {
				return !details.providers.find((f) => {
					return f == e.abbreviation;
				});
			})
			.sort((a: ServiceProvider, b: ServiceProvider) =>
				a.name > b.name ? 1 : b.name > a.name ? -1 : 0
			);
		response = await axios.get('/requests/membership', {
			baseURL: $api.base_url + $api.modules.aai
		});
		if (response.status === 200) {
			openRequests = response.data.filter((e: MembershipRequest) => {
				return e.mail === details.email;
			});
		}
	});
</script>

<svelte:head>
	<title>My Profile</title>
	<meta name="description" content="User Profile" />
	<script src="https://cdn.plot.ly/plotly-latest.min.js" type="text/javascript"></script>
</svelte:head>

<Profile bind:details bind:providers bind:openRequests />
