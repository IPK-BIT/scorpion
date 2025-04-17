<script>
    import axios from "axios";
    import { api } from "../../stores/api";
    import { onMount } from "svelte";
    import { Close } from "carbon-icons-svelte";
    import Select from "../form-elements/Select.svelte";

    let indicators = [];
    let categories = [];

    let indicator = {
        name: '',
        description: '',
        categories: []
    }
    let field = {
        options: [], 
        multiple: true, 
        id: 'kpi-categories', 
        label: 'Categories'
    }

    onMount(async ()=> {
        loadIndicators();
        loadCategories();
    })

    async function loadCategories() {
        const response = await axios.get("/categories", {
            baseURL: $api.base_url+$api.modules.v1
        });
        categories = response.data.result;
        field.options = categories.map(category => ({label: category.name, value: category.name})).sort((a,b) => a.label.localeCompare(b.label));
    }

    async function loadIndicators() {
        const response = await axios.get("/indicators", {
            baseURL: $api.base_url+$api.modules.v1
        });
        indicators = response.data.result;
    }

    let readonly = false;
    let addedCategories = [];
    function openModal(type, i) {
        if (type=='edit') {
            readonly = true;
        }
        if (i) {
            indicator = {
                name: i.name,
                description: i.description,
                categories: i.categories.filter(c=>c.necessity!=null).map(c => c.name)
            };
            field.options = i.categories.filter(c=>c.necessity==null).map(c => ({label: c.name, value: c.name})).sort((a,b) => a.label.localeCompare(b.label));
        }
        const modal = document.getElementById('kpi-modal');
        // @ts-ignore
        modal.showModal();
    }

    function resetModal() {
        readonly = false;
        indicator = {
            name: '',
            description: '',
            categories: []
        }
        field = {
            options: [],
            multiple: true, 
            id: 'kpi-categories', 
            label: 'Categories'
        }
    }
    
    async function submitKPI() {
        const modal = document.getElementById('kpi-modal');
        // @ts-ignore
        modal.close();

        indicator.categories = [];
        field = {
            options: [], 
            multiple: true, 
            id: 'kpi-categories', 
            label: 'Categories'
        }
    }

</script>

<div class="overflow-auto">
    <table class="table">
        <thead>
            <tr class="border-b-2 border-b-base-200">
                <th class="border-r-2 border-r-base-200">Indicator</th>
                {#each categories as category}
                <th class="text-center">{category.name}</th>
                {/each}
                <th class="border-l-2 border-l-base-200">
                    <button class="btn btn-sm hover:btn-accent" on:click={()=>openModal('add', null)}>Add KPI</button>
                </th>
            </tr>
        </thead>
        <tbody>
            {#each indicators as indicator}
            <tr>
                <td class="border-r-2 border-r-base-200">{indicator.name}</td>
                {#each categories as category}
                <td class="text-center">
                    {#if indicator.categories.find(c => c.name === category.name).necessity == "mandatory"}
                    <span class="badge badge-primary">{indicator.categories.find(c => c.name === category.name).necessity}</span>
                    {:else if indicator.categories.find(c => c.name === category.name).necessity == "recommended"}
                    <span class="badge badge-secondary">{indicator.categories.find(c => c.name === category.name).necessity}</span>
                    {:else if indicator.categories.find(c => c.name === category.name).necessity == "optional"}
                    <span class="badge badge-neutral">{indicator.categories.find(c => c.name === category.name).necessity}</span>
                    {:else}
                    <span class="badge text-neutral">-</span>
                    {/if}
                </td>
                {/each}
                <td class="border-l-2 border-l-base-200">
                    <button class="btn btn-sm hover:btn-accent" on:click={()=>openModal('edit', indicator)}>Edit KPI</button>
                </td>
            </tr>
            {/each}
        </tbody>
    </table>
</div>

{#if categories.length > 0}
    <dialog id="kpi-modal" class="modal">
        <div class="modal-box overflow-auto space-y-2 max-h-[calc(100vh-10rem)]">
            <div class="modal-header flex flow-row items-center justify-between">
                <h3>KPI Details - {readonly?'Edit':'Add'}</h3>
                <form method="dialog">
                    <button class="btn btn-circle btn-sm" on:close={resetModal}><Close/></button>
                </form>            
            </div>
            <fieldset class="fieldset bg-base-200 border-base-300 p-4 rounded-box">
                <legend class="fieldset-legend">KPI Definition</legend>

                <label for="kpi-name" class="fieldset-label">Name</label>
                <input readonly={readonly} id="kpi-name" class="input w-full" bind:value={indicator.name}/>

                <label for="kpi-description" class="fieldset-label">Description</label>
                <textarea id="kpi-description" class="textarea w-full" bind:value={indicator.description}></textarea>

                <Select bind:value={addedCategories} bind:field/>
            </fieldset>

            {#if indicator.categories.length > 0 || addedCategories.length > 0}
            <fieldset class="fieldset bg-base-200 border-base-300 p-4 rounded-box">
                <legend class="fieldset-legend">KPI Necessities</legend>

                {#each [...indicator.categories, ...addedCategories].sort() as category}
                <span class="fieldset-label">{category}</span>
                <div class="flex flex-row justify-between bg-base-100 p-2 rounded-lg border border-neutral">
                    <div class="flex flex-row space-x-2 items-center">
                        <input class="radio radio-sm radio-primary" type="radio" id="{category}-mandatory" name="{category}-necessity" value="mandatory" checked />
                        <label for="{category}-mandatory">Mandatory</label>    
                    </div>
                    <div class="flex flex-row space-x-2 items-center">
                        <input class="radio radio-sm radio-primary" type="radio" id="{category}-recommended" name="{category}-necessity" value="recommended"/>
                        <label for="{category}-recommended">Recommended</label>   
                    </div>
                    <div class="flex flex-row space-x-2 items-center">
                        <input class="radio radio-sm radio-primary" type="radio" id="{category}-optional" name="{category}-necessity" value="optional"/>
                        <label for="{category}-optional">Optional</label>
                    </div>
                </div>
                {/each}
            </fieldset>
            <button class="btn btn-primary w-full uppercase" on:click={submitKPI}>Submit</button>
            {/if}
        </div>
    </dialog>
{/if}