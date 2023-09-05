<script lang="ts">
	import { api, serviceOverview } from "$lib/stores/api";
	import axios from "axios";
	import { onMount } from "svelte";
	import KpiTable from "$lib/components/dashboard/KPITable.svelte";
	import KpiTrend from "$lib/components/dashboard/KPITrend.svelte";
	import ServicesOverview from "$lib/components/dashboard/ServicesOverview.svelte";
	import type { Service } from "$lib/stores/types";
		
	onMount(async ()=>{
		const serviceResponse = await axios.get("/services", {
			baseURL: $api.base_url+$api.modules.v1
		})
		if (serviceResponse.status===200) {
			services = serviceResponse.data.result;
		}
		var categories: string[] = [], providers: string[] = [];
		for (let service of services) {
			if (service.provider) {
				!categories.includes(service.category)?categories.push(service.category):null;
				!providers.includes(service.category)?providers.push(service.provider):null;
			}
		}
		serviceOverview.set({categories:categories,providers:providers})
	})
	
	let services: Service[] = []
</script>

<svelte:head>
<title>Home</title>
<meta name="description" content="Service Monitoring KPI Dashboard of NFDI4Biodiversity" />
<script src="https://cdn.plot.ly/plotly-latest.min.js" type="text/javascript"></script>	
</svelte:head>

<div class="pt-4 pb-4 space-y-4">
	<div class="flex flex-row space-x-4 pr-4 pl-4">
		<KpiTable bind:services/>
	</div>
	<div class="flex flex-row space-x-4 pr-4 pl-4">
		<KpiTrend id="kpiTrend" bind:services/>
		<ServicesOverview id="serviceOverview" bind:services/>
		<!--<ServiceProfile bind:services/>-->
	</div>
</div>