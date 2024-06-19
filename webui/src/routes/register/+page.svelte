<script lang="ts">
	import UploadCard from '$lib/components/wizard/UploadCard.svelte';
	import { Close, Warning } from 'carbon-icons-svelte';
	import { metadata, reset, steps } from '$lib/stores/bonsai';
	import axios from 'axios';
	import { api } from '$lib/stores/api';

	let validationErrors: { type: string; message: string }[] = [];

	function validatePage() {
		if (!$metadata.abbreviation) {
			if (validationErrors.find((e) => e.message === 'Abbreviation is missing') === undefined) {
				validationErrors = [
					...validationErrors,
					{ type: 'error', message: 'Abbreviation is missing' }
				];
			}
		}
		if (!$metadata.name) {
			if (validationErrors.find((e) => e.message === 'Name is missing') === undefined) {
				validationErrors = [...validationErrors, { type: 'error', message: 'Name is missing' }];
			}
		}
		if (!$metadata.provider) {
			if (validationErrors.find((e) => e.message === 'Provider is missing') === undefined) {
				validationErrors = [...validationErrors, { type: 'error', message: 'Provider is missing' }];
			}
		}
		if (!$metadata.category) {
			if (validationErrors.find((e) => e.message === 'Category is missing') === undefined) {
				validationErrors = [...validationErrors, { type: 'error', message: 'Category is missing' }];
			}
		}
		return validationErrors.length === 0;
	}

	async function finishRegistration() {
		console.log('metadata', $metadata);
		if (validatePage()) {
			let resp = await axios.post('/bonsai', $metadata, {
				baseURL: $api.base_url + $api.modules.v1
			});
			if (resp.status === 200) {
				reset();
			}
			// reset();
		}
	}
</script>

<svelte:head>
	<title>Service Registration</title>
	<meta name="description" content="Service Registration" />
</svelte:head>

<div class="p-4 flex justify-center">
	<div class="p-4 bg-base-200 rounded-md border border-base-300 w-1/2">
		<UploadCard steps={$steps} on:finish={finishRegistration} />
	</div>
	<div class="absolute right-4 space-y-2">
		{#each validationErrors as error}
			<div class="alert alert-{error.type} w-80">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="stroke-current shrink-0 h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"><Warning size={24} /></svg
				>
				<span>{error.message}</span>
				<button
					on:click={() => {
						validationErrors = validationErrors.filter((e) => {
							return e.message != error.message;
						});
					}}><Close /></button
				>
			</div>
		{/each}
	</div>
</div>
