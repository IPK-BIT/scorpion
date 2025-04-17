<script>
    import { config } from "../../lib/scorpion.config";
    import Select from "../form-elements/Select.svelte";
    import License from "../form-elements/License.svelte";
    import Url from "../form-elements/URL.svelte";

    import { api, token } from "../../stores/api";
    import { onMount } from "svelte";
    import axios from "axios";

    let providers = [];
    onMount(async () => {
        const response = await axios.get(`${$api.base_url}${$api.modules.v1}/providers?is_member=true`);
        providers = response.data.result;
    })
    export let service;
    export let profile_ids = [];
</script>

<fieldset class="fieldset bg-base-200 border border-base-300 p-4 rounded-box">
            <legend class="fieldset-legend">General Information</legend>
            
            <label for="name" class="fieldset-label">
                Service Name
                <p class="text-red-500">*</p>
            </label>
            <input id="name" type="text" class="input w-full" bind:value={service.name}/>
            
            <label for="abbr" class="fieldset-label">
                Abbreviation
                <p class="text-red-500">*</p>
            </label>
            <input id="abbr" type="text" class="input w-full" bind:value={service.abbreviation}/>

            <label for="provider" class="fieldset-label">
                Service Provider
                <p class="text-red-500">*</p>
            </label>
            <select id="provider" class="select w-full" bind:value={service.provider}>
                <option disabled selected value="">Select an option</option>
                {#each providers as provider}
                <option value={provider.abbreviation}>{provider.name}</option>
                {/each}
            </select>
          </fieldset>
        {#each config.service_profiles.filter((profile) => profile_ids.includes(profile.id)) as profile}
        <fieldset class="fieldset bg-base-200 border border-base-300 p-4 rounded-box">
            <legend class="fieldset-legend">{profile.name}</legend>
            {#each profile.fields as field}
            {#if field.type === "text"}
            <input id={field.id} type="text" class="input w-full" />
            {:else if field.type === "url"}
            <Url field={field} />
            {:else if field.type === "select"}
            <Select field={field} bind:value={service[field.jsonPath]}/>
            {:else if field.type === "license"}
            <License field={field} bind:value={service[field.jsonPath]}/>
            {/if}
            {/each}
        </fieldset>
        {/each}

