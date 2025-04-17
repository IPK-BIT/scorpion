<script>
    import { onMount } from "svelte";
    import axios from "axios";
    import { api } from "../stores/api";
    import Card from "../components/Card.svelte";
    import News from "../components/News.svelte";
    import Report from "../components/dashboard/Report.svelte";
    import ServiceInfo from "../components/ServiceInfo.svelte";

	let selectedService;
	let selectedEndDate = new Date().toISOString().slice(0, 7);
	let selectedStartDate = new Date(new Date().setFullYear(new Date().getFullYear() - 1)).toISOString().slice(0, 7);
    let services = [];
	let result_table = [];
	let stats = []
	let activeTab = 0;
	let pageSize = 10;
	let page = 0;
	let totalCount = 0;
	let daily = false;
	let plotDiv;
	let dates = [];
	let kpis;

    onMount(async () => {
		const serviceResponse = await axios.get('/services', {
			baseURL: $api.base_url + $api.modules.v1,
		});
		if (serviceResponse.status === 200) {
			services = serviceResponse.data.result.sort((a, b) => a.name.localeCompare(b.name));
		}
		var categories = [],
			providers = [],
			licenses = [];
		for (let service of services) {
			if (service.category != 'Consortia') {
				if (service.provider) {
					!categories.includes(service.category) ? categories.push(service.category) : null;
					!providers.includes(service.provider) ? providers.push(service.provider) : null;
					if (service.license) {
						!licenses.includes(service.license) ? licenses.push(service.license) : null;
					}
				}
			}
		}
		selectedService = services.filter((s)=>s.category!='Consortia')[0].abbreviation;
		loadKPIs();
	});


	// TODO: handle pagination
	async function loadKPIs() {
		plotDiv = document.getElementById('plot');


		let stop;
		if (selectedEndDate){
			stop = new Date(selectedEndDate);
			stop.setMonth(stop.getMonth()+1);
			stop.setDate(stop.getDate()-1);
		}
		
		let start;
		if (selectedStartDate) {
			start = new Date(selectedStartDate);
		}

		const response = await axios.get('/measurements', {
			baseURL: $api.base_url + $api.modules.v1,
			params: {
				service: selectedService,
				start: start.toISOString(),
				stop: stop.toISOString(),
			},
		});
		if (response.status === 200) {
			let results = response.data.result.sort((a, b) => a.date.localeCompare(b.date));

			result_table = [];
			for (let result of results) {
				let row = result_table.find((r)=>r.date === result.date)
				if (row) {
					row[result.kpi] = result.value;
				} else {
					let new_row = {
						date: result.date,
					}
					new_row[result.kpi] = result.value;
					result_table.push(new_row);
				}
			}
			kpis = Array.from(new Set(result_table.map((r)=>Object.keys(r)).flat())).sort();
			for (let row of result_table) {
				for (let key of kpis) {
					if (!row[key]) {
						console.log(row, key)
						row[key] = null;
					}
				}
			}

			totalCount = result_table.length;

			stats = [];
			if (result_table.length>=2) {
				let last_submission = result_table[result_table.length-1];
				let previous_submission = result_table[result_table.length-2];
				for (let key in last_submission) {
					if (key !== 'date') {
						let last_value = last_submission[key];
						let previous_value = previous_submission[key];
						let percentage = Math.floor(((100*last_value)/previous_value)-100);
						stats = [...stats, {
							name: key,
							value: last_value,
							desc: `${percentage>=0?'+':''}${percentage}% from last submission`,
						}]
					}
				}
			} else if (result_table.length==1) {
				let last_submission = result_table[result_table.length-1];
				for (let key in last_submission) {
					if (key !== 'date') {
						stats = [...stats, {
							name: key,
							value: last_submission[key],
							desc: 'No previous data',
						}]
					}
				}
			}

			let data = [];
			dates = result_table.map((r)=>r.date);
			for (let key of kpis) {
				if (key !== 'date') {
					let trace = {
						x: dates,
						y: result_table.map((r)=>r[key]),
						type: 'scatter',
						mode: 'lines+markers',
						name: key,
					}
					data.push(trace);
				}
			}

			daily=checkDaily(dates);

			// @ts-ignore
			new Plotly.newPlot(plotDiv, data, {
				xaxis: {
					title: 'Date',
				},
				yaxis: {
					title: 'Value',
				},
			}, {
					responsive: true,
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
			});
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
</script>

<div class="w-full px-4 space-y-4">
	<div class="flex flex-row justify-between px-2 items-center">
		<h1 class="text-4xl font-bold">Dashboard</h1>
		<div class="flex flex-row space-x-2">
			<label class="select w-full border-base-300">
				<span class="label">Service</span>
				<select class="w-fit" bind:value={selectedService} on:change={loadKPIs}>
					{#each services as service}
					{#if service.category!='Consortia'}
					<option value={service.abbreviation}>{service.name}</option>
					{/if}
					{/each}
				</select>
			  </label>
			<div class="join border border-base-300 rounded-lg space-x-1">
				<input type="month" class="pl-2 border-none join-item" bind:value={selectedStartDate} on:change={loadKPIs}/>
				<input type="month" class="pr-2 border-none join-item" bind:value={selectedEndDate} on:change={loadKPIs}/>
			</div>
		</div>
	</div>
	<!-- name of each tab group should be unique -->
	<div role="tablist" class="tabs tabs-box w-fit">
		<button class="tab {activeTab===0?'tab-active':''}" role="tab" on:click={()=>activeTab=0}>Overview</button>
		<button class="tab {activeTab===1?'tab-active':''}" role="tab" on:click={()=>activeTab=1}>Tabular</button>
		<button class="tab {activeTab===2?'tab-active':''}" role="tab" on:click={()=>activeTab=2}>Report</button>
	</div>
	<!--TAB OVERVIEW-->
	<div class="{activeTab!=0?'hidden':''} space-y-4">
		<div class="w-full flex flex-row space-x-2">
			{#each stats as stat}
			<div class="stats shadow bg-white w-full">
				<div class="stat">
					<div class="stat-title">{stat.name}</div>
					<div class="stat-value">{stat.value.toLocaleString()}</div>
					<div class="stat-desc">{stat.desc}</div>
				</div>
			</div>
			{/each}
		</div>
		<div class="w-full flex flex-row space-x-2">
			<div class="w-2/3">
				<Card title="Overview">
					<div slot="card-content">
						<div id="plot">
					</div>
				</Card>
			</div>
			<div class="w-1/3">
				<Card title="Service Profile">
					<div slot="card-content">
						<ServiceInfo bind:serviceId={selectedService}/>
					</div>
				</Card>
			</div>
		</div>	
	</div>
	<!--TAB TABULAR-->
	<div class="{activeTab!=1?'hidden':''} space-y-4">
		<div class="w-full flex flex-row space-x-2">
			<Card title="Tabular">
				<div slot="card-content">
					{#if result_table.length>0}
					<table class="table">
						<thead>
							<tr>
								<th>Date</th>
								{#each kpis as key}
								{#if key!='date'}
								<th>{key}</th>
								{/if}								
								{/each}
							</tr>
						</thead>
						<tbody>
							{#each result_table as row, idx}
							{#if idx>=page*pageSize && idx<(page+1)*pageSize}
							<tr class="hover:bg-secondary">
								{#if daily}
								<td>{new Date(row.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric'})}</td>
								{:else}
								<td>{new Date(row.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short' })}</td>
								{/if}
								{#each kpis as key}
								{#if key!='date'}
								<td>{row[key]}</td>
								{/if}
								{/each}
							</tr>
							{/if}
							{/each}
						</tbody>
					</table>
					<div class="flex flex-row w-full space-x-2 justify-center items-center py-2">
						<button class="btn" on:click={() => page = 0} disabled={page == 0}>{"<<"} First</button>
						<button class="btn" on:click={() => page--} disabled={page == 0}>{"<"} Previous</button>
						<select class="select" bind:value={pageSize}>
							<option value={5}>5</option>
							<option value={10}>10</option>
							<option value={12}>12</option>
						</select>
						<button class="btn" on:click={() => page++} disabled={page >= Math.ceil(totalCount/pageSize)-1}>Next {">"}</button>
						<button class="btn" on:click={() => page = Math.ceil(totalCount/pageSize)-1} disabled={page >= Math.ceil(totalCount/pageSize)-1}>Last {">>"}</button>
						<span>Page {page+1} of {Math.ceil(totalCount/pageSize)}</span>
					</div>
					{/if}
				</div>
			</Card>
		</div>
	</div>
	<!--TAB REPORT-->
	<div class="{activeTab!=2?'hidden':''} space-y-4">
		<div class="w-full flex flex-row space-x-2">
			<Card title="Report">
				<div slot="card-content" class="space-y-4">
					<Report bind:result_table bind:daily/>
				</div>
			</Card>
		</div>
	</div>
</div>