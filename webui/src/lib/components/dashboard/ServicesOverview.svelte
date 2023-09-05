<script lang="ts">
	import { serviceOverview } from "$lib/stores/api";
	import type { Service } from "$lib/stores/types";
	import Card from "../pageContents/Card.svelte";
    
    export let id: string;
    export let services: Service[] = [];

    let selectedKind: string|undefined;

    function drawChart() {
        let plotDiv = document.getElementById(id);

        let counts = {};
        if (selectedKind==="category") {
            for (let category of $serviceOverview.categories) {    
                //@ts-ignore
                counts[category]=0;
            }
        } else {
            for (let provider of $serviceOverview.providers) {
                //@ts-ignore
                counts[provider]=0
            }
        }
        
        for (var service of services) {
            //@ts-ignore
            counts[service[selectedKind]]+=1
        }
        console.log(counts);
        console.log(new Set($serviceOverview.providers).values())

        var data = [{
        values: Object.values(counts),
        labels: selectedKind==="category"?$serviceOverview.categories:[...new Set($serviceOverview.providers)],
        type: 'pie'
        }];

        //@ts-ignore
        Plotly.newPlot(plotDiv, data, {});
    }

</script>

<Card title="Services Overview">
    <div  slot="card-content">
        <div class="form-control">
            <label for="service-select" class="label">
                <span class="label-text">Show service distribution by</span>
            </label>
            <select id="service-select" class="select select-bordered" bind:value={selectedKind} on:change={drawChart}>
                <option value={undefined} disabled selected>Pick one</option>
                <option value="category">Category</option>
                <option value="provider">Provider</option>
            </select>
        </div>
        {#if selectedKind}
        <div id={id}/>
        {/if}
    </div>
</Card>