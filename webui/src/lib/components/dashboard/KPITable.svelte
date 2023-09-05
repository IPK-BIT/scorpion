<script lang="ts">
	import { api } from "$lib/stores/api";
	import axios from "axios";
	import Card from "../pageContents/Card.svelte";
	import Table from "../pageContents/Table.svelte";
	import type { Measurement, MeasurementTable, Service } from "$lib/stores/types";
	import { SkipBack, SkipForward } from "carbon-icons-svelte";

    let selectedService: string;
    let measurementTable: MeasurementTable = {
		kpis: [],
		dates: [],
		results: [[]],
		comments: [[]]
	}
	let curPage = 0;
	let pageSize = 12;
	let metadata = {page: 0, pageSize: 0, totalPages: 0, totalCount: 0}

    async function loadKPIs() {
		measurementTable = {
			kpis: [],
			dates: [],
			results: [[]],
			comments: [[]]
		};
		const measurementResponse = await axios.get("/measurements", {
			baseURL: $api.base_url+$api.modules.v1,
			params: {
				service: selectedService,
				page: curPage,
				pageSize: pageSize
			}
		})
		if (measurementResponse.status===200) {
			metadata = measurementResponse.data.metadata;
			measurementResponse.data.result.forEach((element: Measurement) => {
				if(!measurementTable.kpis.includes(element.kpi)) {
					measurementTable.kpis=[...measurementTable.kpis, element.kpi]
				}
				if(!measurementTable.dates.includes(element.date)) {
					measurementTable.dates=[...measurementTable.dates, element.date]
				}
			});
			measurementTable.dates=measurementTable.dates.sort()//.reverse();
			for (let i in measurementTable.dates) {
				for (let j in measurementTable.kpis) {
					let measurement: Measurement = measurementResponse.data.result.find((measurement: Measurement)=>{
						return measurement.date===measurementTable.dates[i] && measurement.kpi===measurementTable.kpis[j]
					})
					if (!measurement) {
						measurement = {kpi: measurementTable.kpis[j], date: measurementTable.dates[i], value:null, comment: null}
					}
					measurementTable.results[i][j]=measurement.value
					measurementTable.comments[i][j]=measurement.comment
				}
				measurementTable.results.push([]);
				measurementTable.comments.push([]);
			}
		}
	}

	async function paginate(newPage: number) {
		if (newPage>=0 && newPage<metadata.totalPages) {
			curPage=newPage;
			loadKPIs();
		}
	}

    export let services: Service[] = [];
</script>

<Card title="KPI Table">
    <div slot="card-content" class="space-y-2">
        <div class="form-control">
            <label for="service-select" class="label">
                <span class="label-text">Pick the service to display the KPIs of</span>
            </label>
            <select id="service-select" class="select select-bordered" bind:value={selectedService} on:change={loadKPIs}>
                <option value={undefined} disabled selected>Pick one</option>
                {#each services as service}
                <option value={service.abbreviation}>{service.name}</option>
                {/each}
            </select>
        </div>
        {#if selectedService}
        <Table bind:kpis={measurementTable.kpis} bind:dates={measurementTable.dates} bind:results={measurementTable.results}></Table>
		<div class="join flex justify-center">
			<button class="join-item btn w-1/6 border-1 border-solid border-neutral" on:click={()=>{paginate(curPage-1)}}><SkipBack/></button>
			<details class="dropdown w-4/6">
				<summary class="join-item btn w-full border-1 border-solid border-neutral">Page {curPage+1}</summary>
				<ul class="p-2 shadow menu dropdown-content z-[1] bg-base-100 rounded-b-box w-full">
				  {#each {length: metadata.totalPages} as _,i}
					<li><button on:click={()=>{paginate(i)}}>Page {i+1}</button></li>
				  {/each}
				</ul>
			  </details>
			<button class="join-item btn w-1/6 border-1 border-solid border-neutral" on:click={()=>{paginate(curPage+1)}}><SkipForward/></button>
		</div>
        {/if}
    </div>
</Card>