<script>
	import { indicators, measurements } from '$lib/stores/consortia';
</script>

<div class="flex flex-col space-y-2">
	{#each $indicators.filter((i) => {
		return i.name.startsWith('2');
	}) as kpi}
		<label for={kpi.name} class="block text-sm font-medium">{kpi.name}</label>
		<input
			id={kpi.name}
			type="number"
			class="input input-sm input-bordered"
			bind:value={$measurements[kpi.name]}
		/>
	{/each}
</div>
