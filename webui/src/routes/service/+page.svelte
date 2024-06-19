<script lang="ts">
	import { api } from '$lib/stores/api';
	import type { KPI, ServiceProvider } from '$lib/stores/types';
	import axios from 'axios';
	import { AddAlt } from 'carbon-icons-svelte';
	import { onMount } from 'svelte';

	let service: string;
	let abbreviation: string;
	let providers: ServiceProvider[] = [];
	let provider: ServiceProvider;
	let categories: string[] = [
		'Databases',
		'Webapplications',
		'Tools',
		'Workflows',
		'Libraries',
		'Support'
	];
	let category: string | undefined = undefined;
	let kpis: KPI[];

	onMount(async () => {
		const response = await axios.get('/providers', {
			baseURL: $api.base_url + $api.modules.v1
		});
		if (response.status === 200) {
			providers = response.data;
		}
		console.log(providers);
	});

	async function loadKPIs() {
		const response = await axios.get(category + '/kpis', {
			baseURL: $api.base_url + $api.modules.v1
		});
		if (response.status === 200) {
			kpis = response.data;
			kpis = [
				...kpis.filter((elem) => {
					return elem.necessity === 'mandatory';
				}),
				...kpis.filter((elem) => {
					return elem.necessity === 'recommended';
				}),
				...kpis.filter((elem) => {
					return elem.necessity === 'optional';
				})
			];
		}
	}
</script>

<h1 class="flex text-lg font-bold p-4 justify-center">Service KPI Set Registration</h1>
<div class="flex justify-center">
	<form class="bg-white p-4 rounded-md w-1/2" on:submit={() => {}}>
		<div class="form-control space-y-2">
			<!-- svelte-ignore a11y-label-has-associated-control -->
			<label class="input-group">
				<span class="w-[20%]">Service</span>
				<input
					type="text"
					placeholder="Enter service name..."
					class="input input-bordered w-[80%]"
					bind:value={service}
				/>
			</label>
			<label class="input-group">
				<span class="w-[20%]">Abbreviation</span>
				<input
					type="text"
					placeholder="Enter service abbreviation..."
					class="input input-bordered w-[80%]"
					bind:value={abbreviation}
				/>
			</label>
			<label class="input-group">
				<span class="w-[20%]">Service Provider</span>
				<select class="select select-bordered w-[80%]" bind:value={provider}>
					<option disabled selected>Select a provider</option>
					{#each providers as p}
						<option value={p.abbreviation}>{p.name}</option>
					{/each}
				</select>
			</label>
			<label class="input-group">
				<span class="w-[20%]">Category</span>
				<select class="select select-bordered w-[80%]" bind:value={category} on:change={loadKPIs}>
					<option disabled selected>Select a category</option>
					{#each categories as category}
						<option>{category}</option>
					{/each}
				</select>
			</label>
			{#if kpis}
				<div class="divider">Mandatory KPIs</div>
				{#each kpis as kpi}
					{#if kpi.necessity === 'mandatory'}
						<div class="form-control">
							<label class="label cursor-pointer">
								<div class="tooltip tooltip-right" data-tip={kpi.description}>
									<span class="label-text">{kpi.name}</span>
								</div>
								<input type="checkbox" checked disabled class="checkbox" />
							</label>
						</div>
					{/if}
				{/each}
				<div class="divider">Recommended KPIs</div>
				{#each kpis as kpi, i}
					{#if kpi.necessity === 'recommended'}
						<div class="form-control">
							<label class="label cursor-pointer">
								<div class="tooltip tooltip-right" data-tip={kpi.description}>
									<span class="label-text">{kpi.name}</span>
								</div>
								<input type="checkbox" checked disabled class="checkbox" />
							</label>
						</div>
					{/if}
				{/each}
				<div class="divider">
					Optional KPIs <button
						disabled
						class="btn btn-ghost btn-xs"
						on:click={() => {
							alert('Yeah!');
						}}><AddAlt /></button
					>
				</div>
				{#each kpis as kpi}
					{#if kpi.necessity === 'optional'}
						<div class="form-control">
							<label class="label cursor-pointer">
								<div class="tooltip tooltip-right" data-tip={kpi.description}>
									<span class="label-text">{kpi.name}</span>
								</div>
								<input type="checkbox" checked disabled class="checkbox" />
							</label>
						</div>
					{/if}
				{/each}
				<input type="submit" class="btn btn-accent" />
			{/if}
		</div>
	</form>
</div>
