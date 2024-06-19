<script lang="ts">
	import { onMount } from 'svelte';
	import axios from 'axios';
	import { api } from '$lib/stores/api';
	import type { Service } from '$lib/stores/types';
	import MeasurementPanel from './MeasurementPanel.svelte';

	let services: Service[] = [];

	onMount(async () => {
		const response = await axios.get('/services', {
			baseURL: $api.base_url + $api.modules.v1
		});
		if (response.status === 200) {
			services = response.data.result;
		}
	});
</script>

<div class="p-4 space-y-2">
	<div class="flex flex-row space-x-2">
		<MeasurementPanel bind:services />
	</div>
</div>
