<script lang="ts">
    import { necessities } from "$lib/stores/admin";
import { api } from "$lib/stores/api";
	import type { KPI, Measurement, MeasurementCollector, Service } from "$lib/stores/types";
    import axios from "axios";
    import { Information } from "carbon-icons-svelte";
    import { onMount } from "svelte";
    
    let services: Service[] = [];
    let selectedService: number;
    
    onMount(async ()=>{
        //TODO add provider-check by user
        const response = await axios.get("/services", {
            baseURL: $api.base_url+$api.modules.v1
        })
        if (response.status===200) {
            services = response.data.result;
        }
    })
    
    let kpis: KPI[];
    async function loadKPI() {
        let service = services[selectedService];
        const response = await axios.get('/indicators', {
            baseURL: $api.base_url+$api.modules.v1,
            params: {
                category: service.category,
                service: service.abbreviation
            }
        })
        if (response.status===200) {
            kpis = response.data.result
            kpis = [
            ...kpis.filter((elem)=>{return elem.categories.find((c)=>{return c.name===services[selectedService].category})?.necessity==="mandatory"}),
            ...kpis.filter((elem)=>{return elem.categories.find((c)=>{return c.name===services[selectedService].category})?.necessity==="recommended"}),
            ...kpis.filter((elem)=>{return elem.categories.find((c)=>{return c.name===services[selectedService].category})?.necessity==="optional"}),
            ...kpis.filter((elem)=>{return elem.selected && elem.categories.find((c)=>{return c.name===services[selectedService].category})?.necessity===null})
            ]
            console.log(kpis)
            measurementCollector.name = service.name;
            for (let kpi of kpis) {
                //@ts-ignore
                measurementCollector[kpi.name] = null;
            }
        }
        console.log(measurementCollector)
    }
    let clickedKPI: number = 0;
    
    let measurementCollector: MeasurementCollector = {};
    let inserted: Measurement[] = [];
    async function sendMeasurement() {
        let service = services[selectedService];
        let body: Measurement[] = [];
        for (let kpi of kpis) {
            //@ts-ignore
            if (measurementCollector[kpi.name]) {
                body.push({
                    kpi: kpi.name,
                    //@ts-ignore
                    date: measurementCollector.date,
                    //@ts-ignore
                    value: measurementCollector[kpi.name],
                    comment: ""
                })
            }
        }
        const response = await axios.post("/measurements", body, {
            baseURL: $api.base_url+$api.modules.v1,
            params: {
                service: service.abbreviation
            }
        })
        response.status===200?inserted = response.data:null;
    }
    
    function removeMsg(msg: Measurement) {
        inserted = inserted.filter((elem)=>{
            return !(JSON.stringify(elem)===JSON.stringify(msg))
        })
    }
</script>

<svelte:head>
<title>Monthly Submission Form</title>
<meta name="description" content="KPI Submission Form" />
<script src="https://cdn.plot.ly/plotly-latest.min.js" type="text/javascript"></script>	
</svelte:head>

<div class="fixed top-16 right-0 z-10 w-1/5 p-4">
    {#each inserted as msg}
    <div class="alert alert-success shadow-lg">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{msg.kpi} on {msg.date}: {msg.value}</span>
            <button on:click={()=>{removeMsg(msg)}}>✕</button>
    </div>
    {/each}
</div>

<h1 class="flex text-lg font-bold p-4 justify-center">Monthly KPI Submission</h1>
<div class="flex justify-center">
    <form class="bg-white p-4 rounded-md w-1/2" on:submit={sendMeasurement}>
        <div class="form-control space-y-2">
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <div class="join">
                <label class="join-item w-[20%] bg-base-300 label">
                    Service
                </label>
                <select class="select select-bordered join-item w-[80%]" bind:value={selectedService} on:change={loadKPI}>
                    <option value={undefined} disabled selected>Pick one</option>
                    {#each services as service, i}
                    <option value={i}>{service.name}</option>
                    {/each}
                </select>
            </div>
            <div class="join">
                <!-- svelte-ignore a11y-label-has-associated-control -->
                <label class="join-item w-[20%] bg-base-300 label">
                    Date
                </label>
                <input type="month" class="join-item input input-bordered w-[80%]" bind:value={measurementCollector.date}/>
            </div>
            {#if kpis}
            <hr>
            {#each kpis as kpi, i}
            <div class="join">
                <!-- svelte-ignore a11y-label-has-associated-control -->
                <!--TODO FIX CODE REPETITION-->
                {#if kpi.categories.find((c)=>{return c.name===services[selectedService].category})?.necessity==="mandatory"}
                <label class="join-item w-[20%] bg-base-300 label">
                    {kpi.name}
                </label>
                {:else if kpi.categories.find((c)=>{return c.name===services[selectedService].category})?.necessity==="recommended"}
                <label class="join-item w-[20%] bg-base-200 label">
                    {kpi.name}
                </label>
                {:else}
                <label class="join-item w-[20%] bg-base-100 label">
                    {kpi.name}
                </label>
                {/if}
                <input type="number" class="join-item input input-bordered w-[75%]" bind:value={measurementCollector[kpi.name]}/>
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <label for="kpi-description" class="join-item btn btn-secondary w-[5%]" on:click={()=>{clickedKPI=i}}><Information/></label>
            </div>
            {/each}
            <input type="submit" class="btn btn-accent"/>
            {/if}
        </div>
    </form>
    {#if kpis}      
    <input type="checkbox" id="kpi-description" class="modal-toggle"/>
    <label for="kpi-description" class="modal cursor-pointer">
        <label class="modal-box relative" for="">
            <h3 class="text-lg font-bold">Description for {kpis[clickedKPI].name}</h3>
            <p class="italic text-sm">Necessity: {kpis[clickedKPI].necessity?kpis[clickedKPI].necessity:"optional"}</p>
            <p>{kpis[clickedKPI].description}</p>
        </label>
    </label>
    {/if}
</div>