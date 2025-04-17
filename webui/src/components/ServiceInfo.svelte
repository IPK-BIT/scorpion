<script>
    import axios from "axios";
    import { api } from "../stores/api";
    import { loadServices } from "../lib/api-client/services";

    export let serviceId;
    let service;
    
    async function loadService(abbreviation) {
        service = (await loadServices(abbreviation))[0];
    }

    $: loadService({'service': serviceId});
</script>

{#if service}
<section>
    <fieldset class="fieldset bg-base-200 border border-base-300 p-4 rounded-box">
        <legend class="fieldset-legend">General Information</legend>

        <label for="name" class="fieldset-label">Service Name</label>
        <p id="name" class="bg-base-200 p-2 border border-base-300 w-full rounded-lg">{service.name}</p>

        <label for="abbr" class="fieldset-label">Service Provider</label>
        <p id="abbr" class="bg-base-200 p-2 border border-base-300 w-full rounded-lg">{service.provider}</p>

        <label for="category" class="fieldset-label">Category</label>
        <p id="category" class="bg-base-200 p-2 border border-base-300 w-full rounded-lg">{service.category}</p>

    </fieldset>

    <fieldset class="fieldset bg-base-200 border border-base-300 p-4 rounded-box">
        <legend class="fieldset-legend">Additional Information</legend>

        <label for="license" class="fieldset-label">License</label>
        <p id="license" class="bg-base-200 p-2 border border-base-300 w-full rounded-lg">{service.license}</p>

        <label for="stage" class="fieldset-label">Development Stage</label>
        <p id="stage" class="bg-base-200 p-2 border border-base-300 w-full rounded-lg">
            {#if service.stage==='dev'}
                Development
            {:else if service.stage==='demo'}
                Prototype
            {:else if service.stage==='prod'}
                Production
            {:else}
                {service.stage}
            {/if}
        </p>

        <label for="consortia" class="fieldset-label">Consortia</label>
        <ul id="consortia" class="bg-base-200 p-2 border border-base-300 w-full rounded-lg list-disc list-inside">
            {#each service.consortia as consortium}
                <li>{consortium}</li>
            {/each}
        </ul>
    </fieldset>
</section>
{/if}