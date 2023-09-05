<script lang="ts">
	import type { Metadata } from "$lib/stores/types";


    export let metadata:Metadata;
</script>

<form class="form-control space-y-2 p-4">
    <div class="join">
        <span class="join-item label px-2 bg-base-300 w-1/6">Contact</span>
        <input type="email" placeholder="Enter mail of support contact..." class="join-item input input-bordered w-5/6" bind:value={metadata.contact} />
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Helpdesk Contact</span>
        <input type="text" placeholder="Enter name of Helpdesk contact..." class="join-item input input-bordered w-5/6" bind:value={metadata.helpdesk} />
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Supported until</span>
        <input type="date" class="join-item input input-bordered w-5/6" bind:value={metadata.supporteduntil} />
    </div>
</form>