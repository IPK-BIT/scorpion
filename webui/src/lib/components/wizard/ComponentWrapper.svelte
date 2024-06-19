<script>
	export let component;
	export let config = {};

	/**
	 * @type {any}
	 */
	let value;
</script>

<svelte:component this={component} bind:value {config} />
