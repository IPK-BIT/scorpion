<script>
    import { onMount } from "svelte";

    export let field;
    export let value;

    onMount(async ()=>{
        const response = await fetch('https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/json/licenses.json');
        const data = await response.json();
        field.options = data.licenses.map((license) => {
            return {
                value: license.licenseId,
                label: license.name
            }
        });
    })
</script>


<label for={field.id} class="fieldset-label">
    {field.label}
    {#if field.required}
    <p class="text-red-500">*</p>
    {/if}
</label>
<select id={field.id} class="select w-full" bind:value>
    <option disabled selected value="">Select an option</option>
    {#each field.options as option}
    <option value={option.value}>{option.label}</option>
    {/each}
</select>