<script lang="ts">
	import { goto } from "$app/navigation";
	import { api, licenses } from "$lib/stores/api";
	import type { Metadata, ServiceProvider } from "$lib/stores/types";
	import axios from "axios";
	import { Information } from "carbon-icons-svelte";
	import { onMount } from "svelte";

    onMount(async ()=>{
        let resp = await axios.get('/providers', {
            baseURL: $api.base_url+$api.modules.v1,
            params: {
                is_member: true
            }
        })
        if (resp.status===200) {
            providers=resp.data.result.sort((a:ServiceProvider,b:ServiceProvider) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
        }
        resp = await axios.get('/spdx/license-list-data/main/json/licenses.json', {
            baseURL: "https://raw.githubusercontent.com",
            headers: {
                "Authorization": null
            }
        })
        if (resp.status===200) {
            licenses.set(resp.data.licenses)
        }
    })
    let providers: ServiceProvider[] = []

    let checked: boolean[] = [false,false,false,false,false,false]
    export let metadata:Metadata;
</script>

<form class="form-control space-y-2 p-4">
    <div class="join">
        <span class="join-item label px-2 bg-base-300 w-1/6">Name</span>
        <input type="text" placeholder="Enter a name..." class="join-item input input-bordered w-5/6" bind:value={metadata.name} />
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-300 w-1/6">Abbreviation</span>
        <input type="text" placeholder="Enter a title..." class="join-item input input-bordered w-5/6" bind:value={metadata.abbreviation} />
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-300 w-1/6">Service Provider</span>
        <select class="join-item w-5/6 select select-bordered" bind:value={metadata.provider}>
            <option value="" selected disabled>Select a Service Provider</option>
            {#each providers as provider}
            <option value={provider.abbreviation}>{provider.name}</option>
            {/each}
        </select>
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Area of Application</span>
        <div class="join-item bg-base-100 w-5/6 p-1 border border-neutral border-opacity-40">
            <div class="form-control">
                <label class="label cursor-pointer">
                    <span class="label-text bg-base-100">Planning</span> 
                    <input type="checkbox" class="checkbox" bind:checked={metadata.areaofapplication.planning}/>
                </label>
            </div>
            <div class="form-control">
                <label class="label cursor-pointer">
                    <span class="label-text bg-base-100">Harmonization</span> 
                    <input type="checkbox" class="checkbox" bind:checked={metadata.areaofapplication.harmonization}/>
                </label>
            </div>
            <div class="form-control">
                <label class="label cursor-pointer">
                    <span class="label-text bg-base-100">Access/Archival</span> 
                    <input type="checkbox" class="checkbox" bind:checked={metadata.areaofapplication.access} />
                </label>
            </div>
            <div class="form-control">
                <label class="label cursor-pointer">
                    <span class="label-text bg-base-100">Discover/Exploration</span> 
                    <input type="checkbox" class="checkbox" bind:checked={metadata.areaofapplication.discover} />
                </label>
            </div>
            <div class="form-control">
                <label class="label cursor-pointer">
                    <span class="label-text bg-base-100">Processing/Visualization</span> 
                    <input type="checkbox" class="checkbox" bind:checked={metadata.areaofapplication.processing} />
                </label>
            </div>
            <div class="form-control">
                <label class="label cursor-pointer">
                    <span class="label-text bg-base-100">Support/Training</span> 
                    <input type="checkbox" class="checkbox" bind:checked={metadata.areaofapplication.support} />
                </label>
            </div>
        </div>
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-300 w-1/6">Description</span>
        <textarea rows={1} placeholder="Enter a description..." class="join-item w-5/6 textarea textarea-bordered" bind:value={metadata.description}/>
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Input Formats</span>
        <input type="text" placeholder="txt, csv, json,..." class="join-item input input-bordered w-5/6" bind:value={metadata.inputformats} />
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Output Formats</span>
        <input type="text" placeholder="txt, csv, json,..." class="join-item input input-bordered w-5/6" bind:value={metadata.outputformats} />
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Development Stage</span>
        <select class="join-item select select-bordered w-5/6" bind:value={metadata.developmentstage}>
            <option value="" disabled selected>Select a Development Stage</option>
            <option>Development</option>
            <option>Demonstrator</option>
            <option>Productive</option>
        </select>
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Version</span>
        <input type="text" placeholder="Enter current version..." class="join-item input input-bordered w-5/6" bind:value={metadata.version} />
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Documentation</span>
        <input type="text" placeholder="Enter link to documentation..." class="join-item input input-bordered w-5/6" bind:value={metadata.documentation} />
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">License</span>
        <select class="join-item w-4/6 select select-bordered" bind:value={metadata.license}>
            <option value="" disabled selected>Select a License</option>
            {#each $licenses as license}
                <option value={license.licenseId}>{license.name}</option>
            {/each}
        </select>
        <a class="join-item bg-secondary w-1/6 btn" target="_blank" href={$licenses.find((l)=>{return l.licenseId===metadata.license})?.seeAlso[0]||""}><Information/>License Info</a>
    </div>
    <div class="join">
        <span class="join-item label px-2 bg-base-200 w-1/6">Link to Service</span>
        <input type="text" placeholder="Enter link to service" class="join-item input input-bordered w-5/6" bind:value={metadata.link} />
    </div>
</form>