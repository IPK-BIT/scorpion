<script lang="ts">
	import { api } from "$lib/stores/api";
	import axios from "axios";
	import Card from "../pageContents/Card.svelte";
	import type { LineChartData, Measurement, MeasurementTable, Service } from "$lib/stores/types";

    export let id: string;
    let plotDiv;

    let selectedService: string;
    let measurements: MeasurementTable = {
		kpis: [],
		dates: [],
		results: [[]],
		comments: [[]]
	}
    let data: LineChartData;

    async function loadKPIs() {
        plotDiv = document.getElementById(id);
		measurements = {
			kpis: [],
			dates: [],
			results: [[]],
			comments: [[]]
		};
		const measurementResponse = await axios.get("/measurements", {
			baseURL: $api.base_url+$api.modules.v1,
            params: {
                service: selectedService,
                start: start?start+"-01T00:00:00Z":null,
                stop: stop?stop+"-01T23:59:59Z":null
            }
		})
		if (measurementResponse.status===200) {
			measurementResponse.data.result.forEach((element: Measurement) => {
				if(!measurements.kpis.includes(element.kpi)) {
					measurements.kpis=[...measurements.kpis, element.kpi]
				}
				if(!measurements.dates.includes(element.date)) {
					measurements.dates=[...measurements.dates, element.date]
				}
			});
			for (let j in measurements.kpis) {
                for (let i in measurements.dates) {
					let measurement: Measurement = measurementResponse.data.result.find((measurement: Measurement)=>{
						return measurement.date===measurements.dates[i] && measurement.kpi===measurements.kpis[j]
					})
					if (!measurement) {
						measurement = {
                            kpi: measurements.kpis[j], 
                            date: measurements.dates[i], 
                            value:null, 
                            comment: null
                        }
					}
					measurements.results[j][i]=measurement.value
					measurements.comments[j][i]=measurement.comment
				}
				measurements.results.push([]);
				measurements.comments.push([]);
			}
            delete measurements.results[measurements.results.length-1];
            delete measurements.comments[measurements.comments.length-1];

            data = [];
            for (let i=0; i<measurements.kpis.length; i++) {
                data = [...data,{
                    y: measurements.results[i], 
                    x: measurements.dates, 
                    name: measurements.kpis[i],
                    mode: 'lines+markers', 
                    connectgaps: true
                }];
            }
            //@ts-ignore
            new Plotly.newPlot(
                plotDiv, 
                data, {}, {
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
            )
		}
	}
    let start: string;
    let stop: string;

    export let services: Service[] = [];
</script>

<Card title="KPI Trend">
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
        <div class="flex">
            <div class="form-control w-1/2">
                <label for="startmonth">Begin in</label>
                <input id="startmonth" type="month" class="input input-bordered w-[80%]" bind:value={start} on:change={loadKPIs}/>
            </div>
            <div class="form-control w-1/2">
                <label for="endmonth">End in</label>
                <input id="endmonth" type="month" class="input input-bordered w-[80%]" bind:value={stop} on:change={loadKPIs}/>
            </div>
        </div>
        {#if selectedService}
        <div id={id}/>
        {/if}
    </div>
</Card>
