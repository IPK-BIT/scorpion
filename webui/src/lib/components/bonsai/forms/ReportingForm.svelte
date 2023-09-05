<script lang="ts">
	import axios from "axios";
	import { api } from "$lib/stores/api";
    import type { KPI, Metadata } from "$lib/stores/types";
	import { AddAlt } from "carbon-icons-svelte";
	import { onMount } from "svelte";

    onMount(async ()=>{
        const response = await axios.get('/indicators', {
            baseURL: $api.base_url+$api.modules.v1,
            params: {
                category: metadata.category
            }
        })
        if (response.status===200) {
            categoryKPI = response.data.result.filter((k:KPI)=>{
                return k.categories.find((c)=>{
                    return c.name===metadata.category
                })?.necessity!=null
            })
            otherKPI = response.data.result.filter((k:KPI)=>{
                return k.categories.find((c)=>{
                    return c.name===metadata.category
                })?.necessity===null
            })
        }
    })

    let categoryKPI: KPI[] = [];
    let otherKPI: KPI[] = [];

    async function loadKPIs() {
        metadata.additionalKPI = [];
        const response = await axios.get('/indicators', {
            baseURL: $api.base_url+$api.modules.v1,
            params: {
                category: metadata.category
            }
        })
        if (response.status===200) {
            categoryKPI = response.data.result.filter((k:KPI)=>{
                return k.categories.find((c)=>{
                    return c.name===metadata.category
                })?.necessity!=null
            })
            otherKPI = response.data.result.filter((k:KPI)=>{
                return k.categories.find((c)=>{
                    return c.name===metadata.category
                })?.necessity===null
            })
        }
    }

    function addAdditional() {
        metadata.additionalKPI=otherKPI.filter((e:KPI)=>{return e.selected})
        metadata.additionalKPI.forEach((e:KPI)=>{e.selected=true})
    }

    function toggleSelected(kpi:KPI) {
        let tmp = otherKPI.find((e:KPI)=>{return e.name===kpi.name})
        if (tmp) {
            tmp.selected=kpi.selected
        }
        otherKPI = otherKPI
    }

    export let metadata:Metadata;
</script>

<form class="form-control space-y-2 p-4">
    <div class="join">
        <span class="join-item label px-2 bg-base-300 w-1/6">Service Category</span>
        <select class="join-item w-5/6 select" bind:value={metadata.category} on:change={loadKPIs}>
            <option disabled selected value="">Please select one category</option>
            <!--TODO Dynamic Categories-->
            <option>Databases</option>
            <option>Tools</option>
            <option>Webapplications</option>
            <option>Libraries</option>
            <option>Workflows</option>
            <option>Supports</option>
            <option>Trainings</option>
        </select>
    </div>
    {#if categoryKPI}
    <div class="divider">Mandatory KPIs</div>
    {#each categoryKPI.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0)) as kpi}
        {#if kpi.categories.find((c)=>{return c.name===metadata.category})?.necessity==="mandatory"}
        <div class="form-control">
            <label class="label cursor-pointer">
                <div class="tooltip tooltip-right" data-tip={kpi.description}>
                    <span class="label-text">{kpi.name}</span>
                </div>
                <input type="checkbox" checked disabled class="checkbox" />
            </label>
        </div>
        {/if}
    {/each}
    <div class="divider">Recommended KPIs</div>
    {#each categoryKPI.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0)) as kpi}
        {#if kpi.categories.find((c)=>{return c.name===metadata.category})?.necessity==="recommended"}
        <div class="form-control">
            <label class="label cursor-pointer">
                <div class="tooltip tooltip-right" data-tip={kpi.description}>
                    <span class="label-text">{kpi.name}</span>
                </div>
                <input type="checkbox" checked disabled class="checkbox" />
            </label>
        </div>
        {/if}
    {/each}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="divider">Optional KPIs <label for="my-modal-3" class="btn btn-ghost btn-xs"><AddAlt/></label></div>
    {#each categoryKPI.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0)) as kpi}
        {#if kpi.categories.find((c)=>{return c.name===metadata.category})?.necessity==="optional"}
        <div class="form-control">
            <label class="label cursor-pointer">
                <div class="tooltip tooltip-right" data-tip={kpi.description}>
                    <span class="label-text">{kpi.name}</span>
                </div>
                <input type="checkbox" checked disabled class="checkbox" />
            </label>
        </div>
        {/if}
    {/each}
    {#each metadata.additionalKPI as kpi}
    <div class="form-control">
        <label class="label cursor-pointer">
            <div class="tooltip tooltip-right" data-tip={kpi.description}>
                <span class="label-text">{kpi.name}</span>
            </div>
            <input type="checkbox" bind:checked={kpi.selected} class="checkbox" on:change={()=>toggleSelected(kpi)}/>
        </label>
    </div>
    {/each}
    {/if}
</form>

<!-- Put this part before </body> tag -->
<input type="checkbox" id="my-modal-3" class="modal-toggle" />
<div class="modal">
    <div class="modal-box relative">
        <label for="my-modal-3" class="btn btn-sm btn-circle absolute right-2 top-2">✕</label>
        <h3 class="text-lg font-bold">Additional KPI Selection</h3>
        <div class="py-4">
            {#each otherKPI.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0)) as kpi}
            <div class="form-control">
                <label class="label cursor-pointer">
                    <div class="tooltip tooltip-right" data-tip={kpi.description}>
                        <span class="label-text">{kpi.name}</span>
                    </div>
                    <input type="checkbox" bind:checked={kpi.selected} class="checkbox checkbox-primary" />
                </label>
            </div>
            {/each}
        </div>
        <div class="modal-action">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <label for="my-modal-3" class="btn btn-primary" on:click={addAdditional}>Add KPI</label>
        </div>
    </div>
</div>