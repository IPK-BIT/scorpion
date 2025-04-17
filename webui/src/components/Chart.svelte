<script lang="ts">
	import { api } from '../stores/api';
	import axios from 'axios';
	import Card from './Card.svelte';

	export let id;
	let plotDiv;

	let selectedService;
	let measurements = {
		kpis: [],
		dates: [],
		results: [[]],
		comments: [[]]
	};
	let data;

	async function loadKPIs() {
		plotDiv = document.getElementById(id);
		measurements = {
			kpis: [],
			dates: [],
			results: [[]],
			comments: [[]]
		};
		const measurementResponse = await axios.get('/measurements', {
			baseURL: $api.base_url + $api.modules.v1,
			params: {
				service: selectedService,
				start: start ? start + '-01T00:00:00Z' : null,
				stop: stop ? stop + '-01T23:59:59Z' : null
			}
		});
		if (measurementResponse.status === 200) {
			measurementResponse.data.result.forEach((element) => {
				if (!measurements.kpis.includes(element.kpi)) {
					measurements.kpis = [...measurements.kpis, element.kpi];
				}
				if (!measurements.dates.includes(element.date)) {
					measurements.dates = [...measurements.dates, element.date];
				}
			});
			for (let j in measurements.kpis) {
				for (let i in measurements.dates) {
					let measurement = measurementResponse.data.result.find(
						(measurement) => {
							return (
								measurement.date === measurements.dates[i] &&
								measurement.kpi === measurements.kpis[j]
							);
						}
					);
					if (!measurement) {
						measurement = {
							kpi: measurements.kpis[j],
							date: measurements.dates[i],
							value: null,
							comment: null
						};
					}
					measurements.results[j][i] = measurement.value;
					measurements.comments[j][i] = measurement.comment;
				}
				measurements.results.push([]);
				measurements.comments.push([]);
			}
			delete measurements.results[measurements.results.length - 1];
			delete measurements.comments[measurements.comments.length - 1];

			data = [];
			for (let i = 0; i < measurements.kpis.length; i++) {
				data = [
					...data,
					{
						y: measurements.results[i],
						x: measurements.dates,
						name: measurements.kpis[i],
						mode: 'bar',
						connectgaps: true
					}
				];
			}
			//@ts-ignore
			new Plotly.newPlot(
				plotDiv,
				data,
				{},
				{
					modeBarButtonsToRemove: [
						'select2d',
						'lasso2d',
						'autoScale2d',
						'zoomIn2d',
						'zoomOut2d',
						'toggleSpikelines',
						'hoverClosestCartesian',
						'pan2d'
					]
				}
			);
		}
	}
	let start;
	let stop;

	export let services = [];
</script>

<Card title="KPI Trend">
	<div slot="card-content" class="space-y-2">
        <div>    
            <label class="select w-fit">
                <span class="label">Service</span>
				<select
					id="service-select"
					bind:value={selectedService}
					on:change={loadKPIs}
				>
					<option value={undefined} disabled selected>Pick one</option>
					{#each services as service}
						<option value={service.abbreviation}>{service.name}</option>
					{/each}
				</select>
            </label>
            <label class="input w-fit" for="startmonth">
                <span class="label">Start Date</span>
				<input
					id="startmonth"
					type="month"
					bind:value={start}
					on:change={loadKPIs}
				/>
            </label>
            <label class="input w-fit" for="endmonth">
                <span class="label">End Date</span>
            <input
                id="endmonth"
                type="month"
                bind:value={stop}
                on:change={loadKPIs}
            />
            </label>
        </div>  
		{#if selectedService}
        <div class="border border-base-200">
            <div {id}></div>
        </div>
		{/if}
	</div>
</Card>