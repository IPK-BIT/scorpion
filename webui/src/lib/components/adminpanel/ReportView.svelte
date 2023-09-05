<script lang="ts">
    import { onMount } from "svelte";
    import Card from "../pageContents/Card.svelte";
	import axios from "axios";
	import { api } from "$lib/stores/api";
	import type { KPI, Measurement, Service } from "$lib/stores/types";
    
    let id="spc-report";
    let services: Service[] = [];
    let selected_service: string = "";
    let indicators: KPI[] = [];
    let selected_indicator: string = "";
    let selected_year: number = 2022;
    let measurements: Measurement[] = [];

    onMount(async ()=>{
        let response = await axios.get('/services', {
            baseURL: $api.base_url+$api.modules.v1
        }) 
        if (response.status===200) {
            services = response.data.result
        }
    })

    async function loadKPI() {
        let response = await axios.get('/indicators', {
            baseURL: $api.base_url+$api.modules.v1,
            params: {
                service: selected_service
            }
        })
        if (response.status===200) {
            indicators = response.data.result
        }
    }

    async function loadMeasurements() {
        let response = await axios.get('/measurements', {
            baseURL: $api.base_url+$api.modules.v1,
            params: {
                service: selected_service,
                indicators: selected_indicator,
                start: selected_year+"-01-01T00:00:00Z",
                stop: selected_year+"-12-31T00:00:00Z"
            }
        })
        if (response.status===200) {
            measurements = response.data.result
            drawChart()
        }
    }
    
    function drawChart() {
        function getSD(array: number[]) {
            const n = array.length;
            const mean = array.reduce((a,b)=>a+b)/n
            return Math.sqrt(array.map(x=>Math.pow(x-mean,2)).reduce((a,b)=>a+b)/n)
        }

        let plotDiv = document.getElementById(id);
        let x_data: string[] = [];
        let y_data: (number|null)[] = [];
        measurements.forEach((m)=>{
            x_data.push(m.date)
            y_data.push(m.value)
        })
        //@ts-ignore
        let avg: number = y_data.filter((x)=>{return x!=null}).reduce((a,b)=>a+b)/y_data.length;
        //@ts-ignore
        let cl_val = 3*getSD(y_data.filter((x)=>{return x!=null}));
        console.log(cl_val)
        let x_viol: string[] = [];
        let y_viol: number[] = [];
        for (const measurement of measurements) {
            if (measurement.value && (measurement.value>(avg+(cl_val)*avg)||measurement.value<(avg-(cl_val)*avg))) {
                x_viol.push(measurement.date),
                y_viol.push(measurement.value)
            }
        }

        var Data = {
            type: 'scatter',
            x: x_data,
            y: y_data,
            mode: 'lines+markers',
            name: 'Data',
            showlegend: true,
            hoverinfo: 'all',
            line: {
                color: 'blue',
                width: 2
            },
            marker: {
                color: 'blue',
                size: 8,
                symbol: 'circle'
            }
        }
        
        var Viol = {
            type: 'scatter',
            x: x_viol,
            y: y_viol,
            mode: 'markers',
            name: 'Violation',
            showlegend: true,
            marker: {
                color: 'rgb(255,65,54)',
                line: {width: 3},
                opacity: 0.5,
                size: 12,
                symbol: 'circle-open'
            }
        }
        var CL = {
            type: 'scatter',
            x: [x_data[0], x_data[x_data.length-1], null, x_data[0], x_data[x_data.length-1]],
            y: [avg-cl_val, avg-cl_val, null, avg+cl_val, avg+cl_val],
            mode: 'lines',
            name: 'LCL/UCL',
            showlegend: true,
            line: {
                color: 'red',
                width: 2,
                dash: 'dash'
            }
        }
        
        var Centre = {
            type: 'scatter',
            x: [x_data[0], x_data[x_data.length-1]],
            y: [avg, avg],
            mode: 'lines',
            name: 'Centre',
            showlegend: true,
            line: {
                color: 'grey',
                width: 2
            }
        }
        console.log(Centre)
        var data = [Data, CL, Centre, Viol]
        
        // layout
        var layout = {
            title: 'Basic SPC Chart',
            xaxis: {
                zeroline: false
            },
            yaxis: {
                //@ts-ignore
                range: [0,Math.max(y_data.filter((x)=>{return x!=null}))],
                zeroline: false
            }
        }
        //@ts-ignore
        Plotly.newPlot(plotDiv, data,layout, {modeBarButtonsToRemove: ["zoom2d","autoScale2d","zoomIn2d","zoomOut2d","select2d", "lasso2d","toggleSpikelines", "hoverClosestCartesian", "hoverCompareCartesian"]});
    }
</script>

<div class="p-4">
    <Card title="Report Card">
        <div slot="card-content" class="space-y-2">
            <div class="form-control flex flex-row space-x-4">
                <select class="select select-bordered w-4/6" bind:value={selected_service} on:change={loadKPI}>
                    <option value="" disabled selected>Select a service</option>
                    {#each services as service}
                        <option value={service.abbreviation}>{service.name}</option>
                    {/each}
                </select>
                <input class="input input-bordered" type="number" min="2015" max="2099" step="1" bind:value={selected_year} on:change={loadMeasurements}/>
            </div>
            {#if selected_service}
            <div class="form-control flex flex-row">
                <select class="select select-bordered w-4/6" bind:value={selected_indicator} on:change={loadMeasurements}>
                    <option value="">Select an indicator</option>
                    {#each indicators.filter((i)=>{return i.selected}) as indicator}
                        <option>{indicator.name}</option>
                    {/each}
                </select>
            </div>
            {/if}
            <div id={id}/>
        </div>
    </Card>
</div>