<script lang="ts">
	import type { Metadata } from "$lib/stores/types";


    export let metadata:Metadata;
</script>

<form class="form-control space-y-2 p-4">
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Service Orientation</span>
        <select class="join-item select border border-neutral border-opacity-40 w-5/6" bind:value={metadata.serviceorientation}>
            <option value="" disabled selected>Select a Service Orientation</option>
            <option value="userfacing">User Facing</option>
            <option value="technical">Technical</option>
        </select>
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Include in Catalog</span>
        <input type="date" class="join-item input input-bordered w-5/6" bind:value={metadata.includeincataglog}/>
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Service provided as part of</span>
        <div class="join-item bg-base-100 w-5/6 p-1 border border-neutral border-opacity-40">
            <div class=" form-control px-2">
                <tr class="join w-full">
                    <td class="w-1/3"><span class="label-text bg-base-100">Institutional Mission</span> </td>
                    <td class="w-1/3"><input type="number" class="input input-bordered input-xs " bind:value={metadata.serviceprovidedas.institutionalMission.percentage}/></td>
                    <td class="w-1/3 flex justify-end"><input type="checkbox" class="checkbox" bind:checked={metadata.serviceprovidedas.institutionalMission.partOf}/></td>
                </tr>
            </div>
            <div class="form-control px-2">
                <tr class="join w-full">
                    <td class="w-1/3"><span class="label-text bg-base-100">Project Funding</span> </td>
                    <td class="w-1/3"><input type="number" class="input input-bordered input-xs " bind:value={metadata.serviceprovidedas.projectFunding.percentage}/></td>
                    <td class="w-1/3 flex justify-end"><input type="checkbox" class="checkbox" bind:checked={metadata.serviceprovidedas.projectFunding.partOf}/></td>
                </tr>
            </div>
            <div class="form-control px-2">
                <tr class="join w-full">
                    <td class="w-1/3"><span class="label-text bg-base-100">Others</span> </td>
                    <td class="w-1/3"><input type="number" class="input input-bordered input-xs " bind:value={metadata.serviceprovidedas.others.percentage}/></td>
                    <td class="w-1/3 flex justify-end"><input type="checkbox" class="checkbox" bind:checked={metadata.serviceprovidedas.others.partOf}/></td>
                </tr>
            </div>
        </div>
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Funding</span>
        <input type="text" placeholder="Provide further information on the funding of the services" class="join-item input input-bordered w-5/6" bind:value={metadata.funding} />
    </div>
</form>