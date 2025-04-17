<script>
    import { onMount } from "svelte";

    export let link;
    export let title;

    let tou = '';
    onMount(async ()=>{
        const response = await fetch(link);
        tou = await response.text();
    })

</script>

<section class="w-full flex flex-col">
    <h1 class="text-3xl font-bold m-auto">{title}</h1>
    <div class="w-2/3 m-auto mb-2">
    {#if tou}
    {@html tou}
    {/if}
    </div>
</section>