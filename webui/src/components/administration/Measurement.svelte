<script>
    import axios from "axios";
    import { api } from "../../stores/api";
    import { onMount } from "svelte";

    let services = [];
    let dates = [];
    let indicators = [];
    let measurements = [];

    let daily = false;

    let service;
    let indicator;
    let start;
    let stop;

    onMount(async ()=>{
        loadServices();
    })

    async function loadServices() {
        const response = await axios.get("/services", {
            baseURL: $api.base_url+$api.modules.v1
        });
        services = response.data.result;
    }

    async function loadIndicators(serviceId) {
        if (!serviceId) return;
        const response = await axios.get(`/indicators`, {
            baseURL: $api.base_url+$api.modules.v1,
            params: {
                category: services.find(s => s.abbreviation == serviceId).category,
                service: serviceId
            }
        });
        indicators = response.data.result;
        console.log(indicators.filter((i)=>i.selected));
    }

    async function loadMeasurements() {
        console.log(service, start, stop);
        if (service) {
            const response = await axios.get(`/measurements`, {
                baseURL: $api.base_url+$api.modules.v1,
                params: {
                    service: service,
                    indicators: indicator?indicator:undefined,
                    start: start?new Date(start).toISOString():undefined,
                    stop: stop?new Date(stop).toISOString():undefined
                }
            });
            measurements = response.data.result.sort((a, b) => a.date.localeCompare(b.date));
            dates = Array.from(new Set(measurements.map(measurement => measurement.date)));
        }      
    }
    
    function checkDaily(dates) {
		for (let date of dates) {
			if (date.substring(8, 10) != '01') {
				return true;
			}
		}
		return false;
	}

    async function deleteMeasurement(date) {
        const response = await axios.delete('/measurements', {
            baseURL: $api.base_url+$api.modules.v1,
            params: {
                service: service,
                start: new Date(date).toISOString(),
                stop: new Date(new Date(date).setDate(2)).toISOString()
            }
        })
        if (response.status === 200) {
            loadMeasurements();
        }
    }

    $: loadIndicators(service);
    
    $: daily = checkDaily(dates);
</script>

<section>
    <div class="bg-neutral p-4 rounded-box border border-base-300 space-y-2">
        <label class="select w-full">
            <span class="label">Service</span>
            <select bind:value={service} on:change={loadMeasurements}>
                <option value={undefined} selected disabled>Select an option</option>
                {#each services as service}
                    <option value={service.abbreviation}>{service.name}</option>
                {/each}
        </label>
        <div class="flex flex-row space-x-2">
            <label class="input w-1/2">
                <span class="label">Start</span>
                <input type="date" bind:value={start} on:change={loadMeasurements}/>
            </label>
            <label class="input w-1/2">
                <span class="label">Stop</span>
                <input type="date" bind:value={stop} on:change={loadMeasurements}/>
            </label>
        </div>
    </div>
    <div class="overflow-auto max-h-[calc(100vh-15rem)]">
        {#if measurements.length > 0}
        <table class="table">
            <thead>
                <tr>
                    <th>Date</th>
                    {#each indicators as indicator}
                    {#if indicator.selected}
                    <th>{indicator.name}</th>
                    {/if}                        
                    {/each}
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {#each dates as date}
                    <tr class="hover:bg-secondary">
                        {#if daily}
                        <td>{new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric'})}</td>
                        {:else}
                        <td>{new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'short' })}</td>
                        {/if}
                        {#each indicators.filter((i)=>i.selected) as indicator}
                        <td>{(measurements.find((m)=>m.kpi===indicator.name && m.date===date))?.value}</td>
                        {/each}
                        <td>
                            <button class="btn btn-sm hover:btn-error uppercase" on:click={()=>deleteMeasurement(date)}>Delete</button>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
        {/if}
    </div>
</section>