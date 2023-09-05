<script lang="ts">
	import type { Metadata } from "$lib/stores/types";


    export let metadata:Metadata;
</script>

<form class="form-control space-y-2 p-4">
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">User Guidance</span>
        <input type="text" placeholder="Is the user provided withsome guidance in terms of best practice, templates and/or workflows?" class="join-item input input-bordered w-5/6" bind:value={metadata.templates} />
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Communication</span>
        <input type="text" placeholder="How are users informed about news and developments?" class="join-item input input-bordered w-5/6" bind:value={metadata.communication} />
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Registered at</span>
        <div class="join-item bg-base-100 w-5/6 p-1 border border-neutral border-opacity-40">
            <div class="form-control px-2">
                <tr class="join w-full">
                    <td class="w-1/3"><span class="label-text bg-base-100">Bio.tools</span></td>
                    <td class="w-1/3"><input class="input input-bordered input-xs " type="url" bind:value={metadata.registered.biotools.url}/></td>
                    <td class="w-1/3 flex justify-end"><input type="checkbox" class="checkbox" bind:checked={metadata.registered.biotools.registered}/></td>
                </tr>
            </div>
            <div class="form-control px-2">
                <tr class="join w-full">
                    <td class="w-1/3"><span class="label-text bg-base-100">DFG RIsources</span></td>
                    <td class="w-1/3"><input class="input input-bordered input-xs " type="url" bind:value={metadata.registered.risources.url}/></td>
                    <td class="w-1/3 flex justify-end"><input type="checkbox" class="checkbox" bind:checked={metadata.registered.risources.registered}/></td>
                </tr>
            </div>
            <div class="form-control px-2">
                <tr class="join w-full">
                    <td class="w-1/3"><span class="label-text bg-base-100">EOSC Marketplace</span></td>
                    <td class="w-1/3"><input class="input input-bordered input-xs " type="url" bind:value={metadata.registered.eosc.url}/></td>
                    <td class="w-1/3 flex justify-end"><input type="checkbox" class="checkbox" bind:checked={metadata.registered.eosc.registered}/></td>
                </tr>
            </div>
            <div class="form-control px-2">
                <tr class="join w-full">
                    <td class="w-1/3"><span class="label-text bg-base-100">FAIRsharing</span></td>
                    <td class="w-1/3"><input class="input input-bordered input-xs " type="url" bind:value={metadata.registered.fairsharing.url}/></td>
                    <td class="w-1/3 flex justify-end"><input type="checkbox" class="checkbox" bind:checked={metadata.registered.fairsharing.registered}/></td>
                </tr>
            </div>
            <div class="form-control px-2">
                <tr class="join w-full">
                    <td class="w-1/3"><span class="label-text bg-base-100">re3data</span></td>
                    <td class="w-1/3"><input class="input input-bordered input-xs " type="url" bind:value={metadata.registered.re3data.url}/></td>
                    <td class="w-1/3 flex justify-end"><input type="checkbox" class="checkbox" bind:checked={metadata.registered.re3data.registered}/></td>
                </tr>
            </div>
            <div class="form-control px-2">
                <tr class="join w-full">
                    <td class="w-1/3"><span class="label-text bg-base-100">Others</span></td>
                    <td class="w-1/3"><input class="input input-bordered input-xs " type="url" bind:value={metadata.registered.others.url}/></td>
                    <td class="w-1/3 flex justify-end"><input type="checkbox" class="checkbox" bind:checked={metadata.registered.others.registered}/></td>
                </tr>
            </div>
        </div>
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Publications</span>
        <input type="text" placeholder="Are there some public information about the service?" class="join-item input input-bordered w-5/6" bind:value={metadata.publications} />
    </div>
</form>