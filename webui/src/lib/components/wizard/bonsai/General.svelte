<script lang="ts">
	import { api } from '$lib/stores/api';
	import { metadata } from '$lib/stores/bonsai';
	import type { ServiceProvider } from '$lib/stores/types';
	import axios from 'axios';
	import { onMount } from 'svelte';

	onMount(async () => {
		let resp = await axios.get('/providers', {
			baseURL: $api.base_url + $api.modules.v1,
			params: {
				is_member: true
			}
		});
		if (resp.status === 200) {
			providers = resp.data.result.sort((a: ServiceProvider, b: ServiceProvider) =>
				a.name > b.name ? 1 : b.name > a.name ? -1 : 0
			);
		}
		resp = await axios.get('/spdx/license-list-data/main/json/licenses.json', {
			baseURL: 'https://raw.githubusercontent.com',
			headers: {
				Authorization: null
			}
		});
		if (resp.status === 200) {
			licenses = resp.data.licenses;
		}
	});
	let licenses: any[] = [];
	let providers: ServiceProvider[] = [];
</script>

<div class="flex flex-col space-y-2">
	<label for="abbreviation" class="block text-sm font-medium">
		Service Abbreviation<span class="text-red-500">*</span>
	</label>
	<input
		id="abbrevation"
		class="input input-sm input-bordered"
		bind:value={$metadata.abbreviation}
	/>
	<label for="name" class="block text-sm font-medium">
		Service Name<span class="text-red-500">*</span>
	</label>
	<input id="name" class="input input-sm input-bordered" bind:value={$metadata.name} />
	<label for="provider" class="block text-sm font-medium">
		Service Provider<span class="text-red-500">*</span>
	</label>
	<select id="provider" class="select select-sm select-bordered" bind:value={$metadata.provider}>
		<option value="" selected disabled>Select a Service Provider</option>
		{#each providers as provider}
			<option value={provider.abbreviation}>{provider.name}</option>
		{/each}
	</select>
	<label for="consortia" class="block text-sm font-medium">Consortia</label>
	<div class="px-2 py-1 space-y-1 bg-base-100 rounded-md">
		{#each ['NFDI4Biodiversity', 'NFDI4Microbiota'] as consortium}
			<label class="flex justify-between">
				<span class="mr-2">{consortium}</span>
				<input
					type="checkbox"
					class="checkbox"
					bind:group={$metadata.consortia}
					value={consortium}
				/>
			</label>
		{/each}
	</div>
	<!-- TODO: License not correctly selected on preset -->
	<label for="license" class="block text-sm font-medium">License</label>
	<select id="license" class="select select-sm select-bordered" bind:value={$metadata.license}>
		<option value="" disabled selected>Select a License</option>
		{#each licenses as license}
			<option value={license.licenseId}>{license.name}</option>
		{/each}
	</select>
	<label for="stage" class="block text-sm font-medium">Stage of Development</label>
	<select id="stage" class="select select-sm select-bordered" bind:value={$metadata.stage}>
		<option value="" disabled selected>Select a Stage</option>
		<option value="development">Development</option>
		<option value="demonstrator">Demonstrator</option>
		<option value="productive">Production</option>
	</select>
</div>
