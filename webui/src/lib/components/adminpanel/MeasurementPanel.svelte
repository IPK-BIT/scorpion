<script lang="ts">
	import type { Measurement, MeasurementTable, Service } from '$lib/stores/types';
	import axios from 'axios';
	import Card from '../pageContents/Card.svelte';
	import { api } from '$lib/stores/api';
	import Table from '../pageContents/Table.svelte';

	export let services: Service[] = [];
	let selected = '';
	let measurementTable: MeasurementTable = {
		kpis: [],
		dates: [],
		results: [[]],
		comments: [[]]
	};
	let metadata;

	async function loadKPIs() {
		const response = await axios.get('/measurements', {
			baseURL: $api.base_url + $api.modules.v1,
			params: {
				service: selected
			}
		});
		if (response.status === 200) {
			metadata = response.data.metadata;
			response.data.result.forEach((element: Measurement) => {
				if (!measurementTable.kpis.includes(element.kpi)) {
					measurementTable.kpis = [...measurementTable.kpis, element.kpi];
				}
				if (!measurementTable.dates.includes(element.date)) {
					measurementTable.dates = [...measurementTable.dates, element.date];
				}
			});
			measurementTable.dates = measurementTable.dates.sort(); //.reverse();
			for (let i in measurementTable.dates) {
				for (let j in measurementTable.kpis) {
					let measurement: Measurement = response.data.result.find((measurement: Measurement) => {
						return (
							measurement.date === measurementTable.dates[i] &&
							measurement.kpi === measurementTable.kpis[j]
						);
					});
					if (!measurement) {
						measurement = {
							kpi: measurementTable.kpis[j],
							date: measurementTable.dates[i],
							value: null,
							comment: null
						};
					}
					measurementTable.results[i][j] = measurement.value;
					measurementTable.comments[i][j] = measurement.comment;
				}
				measurementTable.results.push([]);
				measurementTable.comments.push([]);
			}
		}
	}

	async function removeMeasurements(e: CustomEvent) {
		const response = await axios.delete('/measurements', {
			baseURL: $api.base_url + $api.modules.v1,
			params: {
				service: selected,
				start: e.detail.start,
				stop: e.detail.stop
			}
		});
		if (response.status === 200) {
			console.log(response.data);
		}
		loadKPIs();
	}
</script>

<Card title="Measurement Deletion">
	<div slot="card-content" class="space-y-2">
		<div class="join w-full">
			<label for="serviceselect" class="join-item label bg-base-200 pl-4 w-1/6 border"
				>Service</label
			>
			<select
				id="serviceselect"
				class="join-item select select-bordered w-5/6"
				bind:value={selected}
				on:change={loadKPIs}
			>
				<option value="" disabled selected>Select a Service</option>
				{#each services as service}
					<option value={service.abbreviation}>{service.name}</option>
				{/each}
			</select>
		</div>
		{#if selected}
			<Table
				bind:kpis={measurementTable.kpis}
				bind:dates={measurementTable.dates}
				bind:results={measurementTable.results}
				removable
				on:remove={removeMeasurements}
			/>
		{/if}
	</div>
</Card>
