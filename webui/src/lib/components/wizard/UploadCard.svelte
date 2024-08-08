<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import ComponentWrapper from './ComponentWrapper.svelte';
	import General from './bonsai/General.svelte';
	import Reporting from './bonsai/Reporting.svelte';
	import DataSheet1 from './datasheet/DataSheet1.svelte';
	import DataSheet2 from './datasheet/DataSheet2.svelte';
	import DataSheet3 from './datasheet/DataSheet3.svelte';
	import DataSheet4 from './datasheet/DataSheet4.svelte';

	export let steps;
	let currentStep = 0;

	const components: any = {
		general: General,
		reporting: Reporting,
		datasheet1: DataSheet1,
		datasheet2: DataSheet2,
		datasheet3: DataSheet3,
		datasheet4: DataSheet4
	};

	const eventDispatcher = createEventDispatcher();
	function finish() {
		currentStep = 0;
		eventDispatcher('finish');
	}
</script>

<section class="space-y-4">
	<h2 class="flex justify-center font-medium text-lg">
		Step {currentStep + 1} of {steps.length}: {steps[currentStep].title}
	</h2>
	{#key currentStep}
		{#if steps[currentStep].components}
			<div>
				{#each steps[currentStep].components as component}
					<ComponentWrapper component={components[component.type]} config={component.config} />
				{/each}
			</div>
		{/if}
	{/key}
	<div class="h-8">
		{#if currentStep > 0}
			<button
				class="btn btn-secondary btn-sm float-left"
				on:click|preventDefault={() => {
					currentStep--;
				}}>Previous</button
			>
		{/if}
		{#if currentStep < steps.length - 1}
			<button
				class="btn btn-primary btn-sm float-right"
				on:click|preventDefault={() => {
					currentStep++;
				}}>Next</button
			>
		{:else}
			<button class="btn btn-primary btn-sm float-right" on:click|preventDefault={finish}
				>Submit</button
			>
		{/if}
	</div>
</section>
