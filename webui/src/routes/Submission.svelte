<script>
    import { onMount } from "svelte";
    import Card from "../components/Card.svelte";
    import axios from "axios";
    import { api } from "../stores/api";

    let services = [];
    let selectedService = '';
    let selectedDate = '';

    onMount(async () => {
		let providers = [];
		let response = await axios.get('/details', {
			baseURL: $api.base_url + $api.modules.aai
		});
		if (response.status === 200) {
			providers = response.data.providers;
		}
		if (providers.length > 0) {
			response = await axios.get('/services', {
				baseURL: $api.base_url + $api.modules.v1,
				params: {
					provider: providers.join(',')
				}
			});
			if (response.status === 200) {
				services = response.data.result;
			}
		}
	});

    let kpis = [];
    let measurementCollector = {};
    let measurements = {};
    let indicators = [];

	async function loadKPI() {
		let service = services.find((s)=>s.abbreviation === selectedService);
		const response = await axios.get('/indicators', {
			baseURL: $api.base_url + $api.modules.v1,
			params: {
				category: service.category,
				service: service.abbreviation
			}
		});
		if (response.status === 200) {
			kpis = response.data.result;
			kpis = [
				...kpis.filter((elem) => {
					return (
						elem.categories.find((c) => {
							return c.name === service.category;
						})?.necessity === 'mandatory'
					);
				}),
				...kpis.filter((elem) => {
					return (
						elem.categories.find((c) => {
							return c.name === service.category;
						})?.necessity === 'recommended'
					);
				}),
				...kpis.filter((elem) => {
					return (
						elem.categories.find((c) => {
							return c.name === service.category;
						})?.necessity === 'optional'
					);
				}),
				...kpis.filter((elem) => {
					return (
						elem.selected &&
						elem.categories.find((c) => {
							return c.name === service.category;
						})?.necessity === null
					);
				})
			];
			measurementCollector.name = service.name;
			for (let kpi of kpis) {
				//@ts-ignore
				measurementCollector[kpi.name] = null;
			}
			if (service.category === 'Consortia') {
				indicators = kpis;
				measurements = measurementCollector;
			}
		}
	}
    
    let msg;

    function validate() {
        for (let kpi of kpis) {
            if (!measurementCollector[kpi.name] || measurementCollector[kpi.name] <= 0) {
                msg = { type: 'error', text: `Invalid value for KPI: ${kpi.name}` };
                return false;
            }
        }
        return true;
    }

    async function submit() {
        let service = services.find((s)=>s.abbreviation === selectedService);
        let data = [];

        if (!validate()) {
            return;
        }

        for (let kpi of kpis) {
            if (measurementCollector[kpi.name]) {
                data.push({
                    kpi: kpi.name,
                    value: measurementCollector[kpi.name],
                    date: measurementCollector.date,
                    comment: ''
                });
            }
        }

        const response = await axios.post('/measurements', data, {
            baseURL: $api.base_url + $api.modules.v1,
            params: {
                service: service.abbreviation,
            }
        })
        if (response.status === 200) {
            msg = {type: 'success', text: 'KPIs submitted successfully', kpi: response.data.map((m) => m.kpi)};
        }
    }

    function removeMsg(obj) {
        setTimeout(() => {
            msg = null;
        }, 5000);
    }

    $: removeMsg(msg);

</script>

<div class="absolute top-16 right-2 z-10">
    {#if msg}
    <div role="alert" class="alert alert-{msg.type}">
        <div class="flex flex-col">
            <span>{msg.text}</span>
            <ul class="list-disc list-inside">
                {#each msg.kpi as kpi}
                    <li>{kpi}</li>
                {/each}
            </ul>
        </div>        
      </div>
    {/if}
</div>
<section class="w-full flex justify-center">
    <div class="w-1/2">
        <Card title="KPI Submission Form" >
            <div slot="card-content">
                <fieldset class="fieldset bg-base-200 border border-base-300 p-4 rounded-box">
                    <legend class="fieldset-legend">Submission Details</legend>

                    <label for="name" class="fieldset-label">Service name</label>
                    <select class="select w-full" bind:value={selectedService} on:change={loadKPI}>
                        <option disabled selected value="">Select an option</option>
                        {#each services as service}
                        <option value={service.abbreviation}>{service.name}</option>
                        {/each}
                    </select>

                    <label for="date" class="fieldset-label">Submission Date</label>
                    {#if navigator.userAgent.toLowerCase().includes('firefox')}
                    <div class="alert alert-warning mb-2">
                        <span>Note: Date input may not be fully supported in Firefox. Please ensure the format is correct. <i class="italic">(YYYY-MM)</i></span>
                    </div>
                    {/if}
                    <input type="month" class="input w-full" bind:value={measurementCollector.date} />
                </fieldset>

                {#if kpis.length>0}
                <fieldset class="fieldset bg-base-200 border border-base-300 p-4 rounded-box">
                    <legend class="fieldset-legend">Service KPI Set</legend>
                    
                    <fieldset class="fieldset bg-base-100 border border-base-300 p-4 rounded-box">
                        <legend class="fieldset-legend">Mandatory KPIs</legend>
                        {#each kpis as kpi}
                        {#if kpi.categories.find((c) => c.name==services.find((s)=>s.abbreviation === selectedService).category).necessity==='mandatory'}
                        <label class="floating-label">
                            <span>{kpi.name}</span>
                            <input type="number" min="0" placeholder={kpi.name} class="input input-md w-full" bind:value={measurementCollector[kpi.name]} />
                          </label>
                        {/if}
                        {/each}
                    </fieldset>
                    <fieldset class="fieldset bg-base-100 border border-base-300 p-4 rounded-box">
                        <legend class="fieldset-legend">Recommended KPIs</legend>
                        {#each kpis as kpi}
                        {#if kpi.categories.find((c) => c.name==services.find((s)=>s.abbreviation === selectedService).category).necessity==='recommended'}
                        <label class="floating-label">
                            <span>{kpi.name}</span>
                            <input type="number" min="0" placeholder={kpi.name} class="input input-md w-full" bind:value={measurementCollector[kpi.name]} />
                          </label>
                        {/if}
                        {/each}
                    </fieldset>
                    <fieldset class="fieldset bg-base-100 border border-base-300 p-4 rounded-box">
                        <legend class="fieldset-legend">Optional KPIs</legend>
                        {#each kpis as kpi}
                        {#if kpi.categories.find((c) => c.name==services.find((s)=>s.abbreviation === selectedService).category).necessity==='optional' || kpi.categories.find((c) => c.name==services.find((s)=>s.abbreviation === selectedService).category).necessity===null}
                        <label class="floating-label">
                            <span>{kpi.name}</span>
                            <input type="number" min="0" placeholder={kpi.name} class="input input-md w-full" bind:value={measurementCollector[kpi.name]} />
                          </label>
                        {/if}
                        {/each}
                    </fieldset>
                </fieldset>
                <div class="py-2">
                    <button disabled={!measurementCollector.date} class="btn btn-primary w-full uppercase" on:click={submit}>Submit</button>
                </div>
                {/if}
            </div>
        </Card>
    </div>
</section>