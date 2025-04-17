<script>
    export let field;
</script>

<label for={field.id} class="fieldset-label">
    {field.label}
    {#if field.required}
    <p class="text-red-500">*</p>
    {/if}
</label>
<input id={field.id} type="url" class="input w-full validator" pattern={field.pattern}/>
<p class="validator-hint">Please enter a valid URL</p>