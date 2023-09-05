<script lang="ts">
	import type { Metadata } from "$lib/stores/types";


    export let metadata:Metadata;
</script>

<form class="form-control space-y-2 p-4">
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Technical Backbone</span>
        <textarea rows={1} placeholder="Enter a description..." class="join-item w-5/6 textarea textarea-bordered" bind:value={metadata.technicalbackbone}/>
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Disaster & Recovery Plan</span>
        <textarea rows={1} placeholder="Enter a description..." class="join-item w-5/6 textarea textarea-bordered" bind:value={metadata.disasterplan}/>
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Entrance Control to Technical Backbone</span>
        <textarea rows={1} placeholder="Enter a description..." class="join-item w-5/6 textarea textarea-bordered" bind:value={metadata.entrancecontrol}/>
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Stability of Operation</span>
        <textarea rows={1} placeholder="Enter a description..." class="join-item w-5/6 textarea textarea-bordered" bind:value={metadata.operationstability}/>
    </div>
</form>