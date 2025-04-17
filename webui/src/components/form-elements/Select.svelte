<script>
    export let field;
    export let value;
    let select = [];
    let deselect = [];

    function doSelect(item) {
        if (select.includes(item)) {
            select = select.filter((i) => i !== item);
        } else {
            select = [...select, item];
        }
    }

    function doDeselect(item) {
        if (deselect.includes(item)) {
            deselect = deselect.filter((i) => i !== item);
        } else {
            deselect = [...deselect, item];
        }
    }

    function moveSelect() {
        let filtered = field.options.filter((option) => select.includes(option.value));
        selected = [...selected, ...filtered].sort((a,b) => a.label.localeCompare(b.label));
        options = options.filter((option) => !select.includes(option.value));
        select = [];
    }
    
    function moveAllDeselect() {
        options = [...options, ...selected].sort((a,b) => a.label.localeCompare(b.label));
        selected = [];
    }

    function moveAllSelect() {
        selected = [...selected, ...options].sort((a,b) => a.label.localeCompare(b.label));
        options = [];    
    }

    function moveDeselect() {
        let filtered = selected.filter((option) => deselect.includes(option.value));
        options = [...options, ...filtered].sort((a,b) => a.label.localeCompare(b.label));
        selected = selected.filter((option) => !deselect.includes(option.value));
        deselect = [];
    }

    let options = field.options;
    let selected=[];

    $: options = field.options;
    
    function updateMultiValue(selected) {
        if (field.multiple) {
            value = selected.map((option) => option.value);
        }        
    }

    $: updateMultiValue(selected);
</script>


<label for={field.id} class="fieldset-label">
    {field.label}
    {#if field.required}
    <p class="text-red-500">*</p>
    {/if}
</label>
{#if field.multiple}
<div id={field.id} class="flex flex-row h-24 bg-base-100 rounded-md border border-neutral-400">
    <ul class="overflow-auto w-1/2 p-2">
        {#each options as option}
            <li class="{select.includes(option.value)?'bg-accent':''}"><button on:click={()=>{doSelect(option.value)}}><p>{option.label}</p></button></li>
        {/each}
    </ul>
    <div class="flex flex-col">
        <button class="btn btn-xs btn-ghost" on:click={moveAllSelect}>{">>"}</button>
        <button class="btn btn-xs btn-ghost" on:click={moveSelect}>{">"}</button>
        <button class="btn btn-xs btn-ghost" on:click={moveDeselect}>{"<"}</button>
        <button class="btn btn-xs btn-ghost" on:click={moveAllDeselect}>{"<<"}</button>
    </div>
    <ul class="overflow-auto w-1/2">
        {#each selected as option}
            <li class="{deselect.includes(option.value)?'bg-accent':''}"><button on:click={()=>{doDeselect(option.value)}}><p>{option.label}</p></button></li>
        {/each}
    </ul>
</div>
{:else}
<select id={field.id} class="select w-full" bind:value>
    <option disabled selected value="">Select an option</option>
    {#each field.options as option}
    <option value={option.value}>{option.label}</option>
    {/each}
</select>
{/if}