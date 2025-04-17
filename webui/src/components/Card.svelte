<script lang="ts">
	export let title = "";
</script>

<div class="card w-full bg-white shadow-md h-fit border border-base-200">
	<div class="card-body">
        {#if title}
		<h2 class="card-title mb-4">{title}</h2>
        {/if}
		<slot name="card-content" />
	</div>
</div>