<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let isLast: boolean = false;
    export let isFirst: boolean = false;
    export let title: string = "Title";

    const dispatch = createEventDispatcher();
    function sendPrevious(){dispatch('previous')};
    function sendNext(){dispatch('next')};
    function sendFinish(){dispatch('finish')};
</script>

<div class="card bg-white shadow-xl h-full w-7/12">
    <div class="card-body">
        <h2 class="card-title">{title}</h2>
        <slot name="card-content"/>
    </div>
    <div class="bottom-0 p-4">
        {#if !isFirst}
        <button class="btn btn-secondary float-left" on:click={sendPrevious}>Previous</button>
        {/if}
        {#if isLast}
        <button class="btn btn-primary float-right" on:click={sendFinish}>Finish</button>
        {:else}
        <button class="btn btn-primary float-right" on:click={sendNext}>Next</button>
        {/if}
    </div>
</div>