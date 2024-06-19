<script lang="ts">
	export let title: string;
</script>

<div class="card w-full bg-white shadow-xl h-fit">
	<div class="card-body">
		<h2 class="card-title mb-4">{title}</h2>
		<slot name="card-content" />
	</div>
</div>
