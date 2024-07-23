<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';

	export let kpis: string[] = [];
	export let dates: string[] = [];
	export let results: (number | null)[][] = [[]];
	export let removable: boolean = false;
	let daily = false;

	const dispatch = createEventDispatcher();
	function sendRemove(date: string) {
		let start = new Date(date).toISOString();
		let stop = new Date(new Date(date).setDate(2)).toISOString();
		dispatch('remove', { start: start, stop: stop });
	}

	function checkDaily() {
		for (let date of dates) {
			if (date.substring(8,10)!='01') {
				return true;
			}
		}
		return false;
	}
</script>

<div class="overflow-x-auto rounded-md">
	<table class="table table-md w-full">
		<thead class="bg-base-300 text-center">
			<tr>
				<th>Date</th>
				{#each kpis as kpi}
					<th>{kpi}</th>
				{/each}
				{#if removable}
					<th />
				{/if}
			</tr>
		</thead>
		<tbody>
			{#each dates as date}
				<tr class="hover text-center">
					{#if checkDaily()}
					<td class="font-semibold bg-base-300"
						>{new Date(date).toLocaleDateString('en', { year: 'numeric', month: 'short', day: 'numeric' })}</td
					>
					{:else}
					<td class="font-semibold bg-base-300"
						>{new Date(date).toLocaleDateString('en', { year: 'numeric', month: 'short' })}</td
					>
					{/if}
					{#each results[dates.findIndex((x) => {
							return x === date;
						})] as result}
						<td>{result}</td>
					{/each}
					{#if removable}
						<td>
							<button
								class="btn btn-sm btn-ghost hover:btn-error"
								on:click={() => {
									sendRemove(date);
								}}>Delete</button
							>
						</td>
					{/if}
				</tr>
			{/each}
		</tbody>
	</table>
</div>
