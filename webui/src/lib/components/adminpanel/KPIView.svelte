<script lang="ts">
	import { onMount } from 'svelte';
	import axios from 'axios';
	import { api } from '$lib/stores/api';
	import { indicators } from '$lib/stores/admin';
	import { Add, Close, SkipBack, SkipForward } from 'carbon-icons-svelte';
	import type { KPI } from '$lib/stores/types';

	onMount(async () => {
		let response = await axios.get('/indicators', {
			baseURL: $api.base_url + $api.modules.v1,
			params: {
				page: curPage,
				pageSize: pageSize
			}
		});
		if (response.status === 200) {
			totalPages = response.data.metadata.totalPages;
			indicators.set(
				response.data.result.sort((a: KPI, b: KPI) =>
					a.name > b.name ? 1 : b.name > a.name ? -1 : 0
				)
			);
		}
	});

	let curPage = 0;
	let pageSize = 10;
	let totalPages = 0;

	let selected_kpi: {
		name: string;
		description: string | null;
		categories: {
			name: string;
			necessity: {
				mandatory: boolean;
				recommended: boolean;
				optional: boolean;
			};
		}[];
	} = {
		name: '',
		description: '',
		categories: []
	};

	function setSelected(indicator: KPI) {
		let categories: {
			name: string;
			necessity: { mandatory: boolean; recommended: boolean; optional: boolean };
		}[] = [];
		indicator.categories.forEach((i) => {
			categories.push({
				name: i.name,
				necessity: {
					mandatory: i.necessity === 'mandatory',
					recommended: i.necessity === 'recommended',
					optional: i.necessity === 'optional'
				}
			});
		});
		selected_kpi = {
			name: indicator.name,
			description: indicator.description,
			categories: categories
		};
	}

	async function paginate(direction: 'backward' | 'forward') {
		if (direction === 'forward' && curPage + 1 < totalPages) {
			curPage += 1;
		} else if (direction === 'backward' && curPage - 1 >= 0) {
			curPage -= 1;
		}
		let response = await axios.get('/indicators', {
			baseURL: $api.base_url + $api.modules.v1,
			params: {
				page: curPage,
				pageSize: pageSize
			}
		});
		if (response.status === 200) {
			totalPages = response.data.metadata.totalPages;
			indicators.set(
				response.data.result.sort((a: KPI, b: KPI) =>
					a.name > b.name ? 1 : b.name > a.name ? -1 : 0
				)
			);
		}
	}
</script>

<div class="p-4 bg-white">
	{#if $indicators.length > 0}
		<table class="table table-pin-rows rounded-md p-4">
			<thead>
				<tr>
					<th>Name</th>
					<th>Description</th>
					{#each $indicators[0].categories as category}
						<th>{category.name}</th>
					{/each}
					<th><button class="btn btn-ghost btn-xs">Add <Add /></button></th>
				</tr>
			</thead>
			<tbody>
				{#each $indicators as indicator}
					<tr class="hover">
						<td>{indicator.name}</td>
						<td>{indicator.description}</td>
						{#each indicator.categories as category}
							<td>
								{#if category.necessity != null}
									<span
										class="badge {category.necessity === 'mandatory'
											? 'badge-primary'
											: category.necessity === 'recommended'
											? 'badge-secondary'
											: 'badge-accent'}">{category.necessity}</span
									>
								{/if}
							</td>
						{/each}
						<td
							><button
								class="btn btn-ghost btn-xs"
								onclick="my_modal_3.showModal()"
								on:click={() => {
									setSelected(indicator);
								}}>Actions</button
							></td
						>
					</tr>
				{/each}
			</tbody>
		</table>
		<div class="join w-full">
			<button
				class="join-item border-neutral btn w-1/6"
				on:click={() => {
					paginate('backward');
				}}><SkipBack /></button
			>
			<button class="join-item border-neutral btn w-2/3">Page {curPage + 1}</button>
			<button
				class="join-item border-neutral btn w-1/6"
				on:click={() => {
					paginate('forward');
				}}><SkipForward /></button
			>
		</div>
	{/if}
</div>

<dialog id="my_modal_3" class="modal">
	<form method="dialog" class="modal-box w-11/12 max-w-5xl">
		<button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
			><Close size={24} /></button
		>
		<h3 class="font-bold text-lg">{selected_kpi.name}</h3>
		<p>{selected_kpi.description}</p>
		<div>
			<table class="table">
				<!-- head -->
				<thead>
					<tr>
						<th>Category</th>
						<th>mandatory</th>
						<th>recommended</th>
						<th>optional</th>
					</tr>
				</thead>
				<tbody>
					{#each selected_kpi.categories as category}
						<tr class="hover">
							<th>{category.name}</th>
							<td
								><input
									disabled
									type="checkbox"
									id="radio-{category.name}"
									class="radio"
									bind:checked={category.necessity.mandatory}
									on:change={() => {
										category.necessity.recommended = false;
										category.necessity.optional = false;
										category = category;
									}}
								/></td
							>
							<td
								><input
									disabled
									type="checkbox"
									id="radio-{category.name}"
									class="radio"
									bind:checked={category.necessity.recommended}
									on:change={() => {
										category.necessity.mandatory = false;
										category.necessity.optional = false;
										category = category;
									}}
								/></td
							>
							<td
								><input
									disabled
									type="checkbox"
									id="radio-{category.name}"
									class="radio"
									bind:checked={category.necessity.optional}
									on:change={() => {
										category.necessity.recommended = false;
										category.necessity.mandatory = false;
										category = category;
									}}
								/></td
							>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</form>
</dialog>
