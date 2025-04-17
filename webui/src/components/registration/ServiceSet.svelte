<script>
	import axios from 'axios';
	import { api } from '../../stores/api';
	import { AddAlt } from 'carbon-icons-svelte';
	import { onMount } from 'svelte';

	let categories = [];

	export let service;

	onMount(async () => {
		let response = await axios.get('/categories', {
			baseURL: $api.base_url+$api.modules.v1,
		}); 
		categories = response.data.result;
		response = await axios.get('/indicators', {
			baseURL: $api.base_url + $api.modules.v1,
			params: {
				category: service.category
			}
		});
		if (response.status === 200) {
			categoryKPI = response.data.result.filter((k) => {
				return (
					k.categories.find((c) => {
						return c.name === service.category;
					})?.necessity != null
				);
			});
			otherKPI = response.data.result.filter((k) => {
				return (
					k.categories.find((c) => {
						return c.name === service.category;
					})?.necessity === null
				);
			});
		}
	});

	let categoryKPI = [];
	let otherKPI = [];

	async function loadKPIs() {
		service.additionalKPI = [];
		const response = await axios.get('/indicators', {
			baseURL: $api.base_url + $api.modules.v1,
			params: {
				category: service.category
			}
		});
		if (response.status === 200) {
			categoryKPI = response.data.result.filter((k) => {
				return (
					k.categories.find((c) => {
						return c.name === service.category;
					})?.necessity != null
				);
			});
			otherKPI = response.data.result.filter((k) => {
				return (
					k.categories.find((c) => {
						return c.name === service.category;
					})?.necessity === null
				);
			});
		}
	}

	function addAdditional() {
		service.additionalKPI = otherKPI.filter((e) => {
			return e.selected;
		});
		service.additionalKPI.forEach((e) => {
			e.selected = true;
		});
	}

	function toggleSelected(kpi) {
		let tmp = otherKPI.find((e) => {
			return e.name === kpi.name;
		});
		if (tmp) {
			tmp.selected = kpi.selected;
		}
		otherKPI = otherKPI;
	}
</script>

<fieldset class="fieldset w-full bg-base-200 border border-base-300 p-4 rounded-box">
    <legend class="fieldset-legend">Service KPIs</legend>

	<label for="category" class="fieldset-label">
		Service Category
		<p class="text-red-500">*</p>
	</label>
	<select
		id="category"
		class="select w-full"
		bind:value={service.category}
		on:change={loadKPIs}
	>
		<option disabled selected value="">Select an option</option>
		{#each categories as categoryOption}
		{#if categoryOption.name != 'Consortia'}
			<option>{categoryOption.name}</option>
		{/if}
		{/each}
	</select>
	{#if categoryKPI}
		<!-- <div class="divider">Mandatory KPIs</div> -->
         <fieldset class="fieldset bg-base-100 border border-base-300 p-4 rounded-box">
            <legend class="fieldset-legend">Service KPI Set</legend>
            
            <label for="mandatory-kpis" class="fieldset-label">Mandatory KPIs</label>
		{#each categoryKPI.sort((a, b) => (a.name > b.name ? 1 : b.name > a.name ? -1 : 0)) as kpi}
			{#if kpi.categories.find((c) => {
				return c.name === service.category;
			})?.necessity === 'mandatory'}
				<div class="bg-base-200 border border-base-300 p-4 rounded-md w-full">
					<label class="label cursor-pointer flex justify-between">
						<div class="tooltip tooltip-right" data-tip={kpi.description}>
							<span class="label-text">{kpi.name}</span>
						</div>
						<input type="checkbox" checked disabled class="checkbox" />
					</label>
				</div>
			{/if}
		{/each}
        <label for="mandatory-kpis" class="fieldset-label">Recommended KPIs</label>
        {#each categoryKPI.sort((a, b) => (a.name > b.name ? 1 : b.name > a.name ? -1 : 0)) as kpi}
			{#if kpi.categories.find((c) => {
				return c.name === service.category;
			})?.necessity === 'recommended'}
				<div class="bg-base-200 border border-base-300 p-4 rounded-md w-full">
					<label class="label cursor-pointer flex justify-between">
						<div class="tooltip tooltip-right" data-tip={kpi.description}>
							<span class="label-text">{kpi.name}</span>
						</div>
						<input type="checkbox" checked disabled class="checkbox" />
					</label>
				</div>
			{/if}
		{/each}
        <label for="mandatory-kpis" class="fieldset-label">Optional KPIs <label for="my-modal-3" class="btn btn-ghost btn-xs btn-circle text-primary"><AddAlt /></label></label>
        {#each categoryKPI.sort((a, b) => (a.name > b.name ? 1 : b.name > a.name ? -1 : 0)) as kpi}
			{#if kpi.categories.find((c) => {
				return c.name === service.category;
			})?.necessity === 'optional'}
				<div class="bg-base-200 border border-base-300 p-4 rounded-md w-full">
					<label class="label cursor-pointer flex justify-between">
						<div class="tooltip tooltip-right" data-tip={kpi.description}>
							<span class="label-text">{kpi.name}</span>
						</div>
						<input type="checkbox" checked disabled class="checkbox" />
					</label>
				</div>
			{/if}
		{/each}
		{#each service.additionalKPI as kpi}
        <div class="bg-base-200 border border-base-300 p-4 rounded-md w-full">
            <label class="label cursor-pointer flex justify-between">
                <div class="tooltip tooltip-right" data-tip={kpi.description}>
                    <span class="label-text">{kpi.name}</span>
                </div>
					<input
						type="checkbox"
						bind:checked={kpi.selected}
						class="checkbox"
						on:change={() => toggleSelected(kpi)}
					/>
				</label>
			</div>
		{/each}
        </fieldset>
    {/if}
</fieldset>

<input type="checkbox" id="my-modal-3" class="modal-toggle" />
<div class="modal">
	<div class="modal-box relative">
		<label for="my-modal-3" class="btn btn-sm btn-circle absolute right-2 top-2">✕</label>
		<h3 class="text-lg font-bold">Additional KPI Selection</h3>
		<div class="py-4 space-y-2">
			{#each otherKPI.sort((a, b) => (a.name > b.name ? 1 : b.name > a.name ? -1 : 0)) as kpi}
				{#if !/^[0-9]/.test(kpi.name[0])}
                <div class="bg-base-200 border border-base-300 p-4 rounded-md w-full">
                    <label class="label cursor-pointer flex justify-between">
							<div class="tooltip tooltip-right" data-tip={kpi.description}>
								<span class="label-text">{kpi.name}</span>
							</div>
							<input
								type="checkbox"
								bind:checked={kpi.selected}
								class="checkbox checkbox-primary"
							/>
						</label>
					</div>
				{/if}
			{/each}
		</div>
		<div class="modal-action">
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
			<label for="my-modal-3" class="btn btn-primary btn-sm" on:click={addAdditional}>Add KPI</label
			>
		</div>
	</div>
</div>