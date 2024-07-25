<script lang="ts">
	import { serviceOverview } from '$lib/stores/api';
	import type { Service } from '$lib/stores/types';
	import Card from '../pageContents/Card.svelte';

	export let id: string;
	export let services: Service[] = [];

	let selectedConsortia: string | undefined;
	let selectedKind: string | undefined;

	function drawChart() {
		let plotDiv = document.getElementById(id);

		let counts = {};
		var labels: string[] = [];
		if (selectedKind === 'category') {
			for (let category of $serviceOverview.categories) {
				//@ts-ignore
				counts[category] = 0;
			}
			labels = $serviceOverview.categories;
		} else if (selectedKind === 'provider') {
			for (let provider of $serviceOverview.providers) {
				//@ts-ignore
				counts[provider] = 0;
			}
			labels = $serviceOverview.providers;
		} else if (selectedKind === 'license') {
			for (let license of $serviceOverview.licenses) {
				//@ts-ignore
				counts[license] = 0;
			}
			labels = $serviceOverview.licenses;
		}

		let filteredServices = services;
		if (selectedConsortia) {
			//@ts-ignore
			filteredServices = services.filter(service => service.consortia.includes(selectedConsortia));
		}
		for (var service of filteredServices) {
			//@ts-ignore
			counts[service[selectedKind]] += 1;
		}
		
		//@ts-ignore
		labels = labels.filter(label => counts[label] > 0);

		counts = Object.fromEntries(
			Object.entries(counts).filter(([key, value]) => labels.includes(key))
		);

		var data = [
			{
				values: Object.values(counts),
				labels: labels,
				type: 'pie'
			}
		];

		//@ts-ignore
		Plotly.newPlot(plotDiv, data, {});
	}
</script>

<Card title="Services Overview">
	<div slot="card-content">
		<div class="form-control">
			<label for="service-select" class="label">
				<span class="label-text">Show service distribution by</span>
			</label>
			<select
				id="service-select"
				class="select select-bordered"
				bind:value={selectedKind}
				on:change={drawChart}
			>
				<option value={undefined} disabled selected>Pick one</option>
				<option value="category">Category</option>
				<option value="provider">Provider</option>
				<option value="license">License</option>
			</select>
		</div>
		<div class="form-control">
			<label for="consortia-select" class="label">
				<span class="label-text">Filtered by consortia</span>
			</label>
			<select 
				id="consortia-select" 
				class="select select-bordered"
				bind:value={selectedConsortia}
				on:change={drawChart}>
				<option value={undefined}>All</option>
				<option value="NFDI4Biodiversity">NFDI4Biodiversity</option>
				<option value="NFDI4Microbiota">NFDI4Microbiota</option>
			</select>
		</div>
		{#if selectedKind}
			<div {id} />
		{/if}
	</div>
</Card>
