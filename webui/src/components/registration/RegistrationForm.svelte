<script>
    import ServiceProfile from "./ServiceProfile.svelte";
    import Card from "../Card.svelte";
    import ServiceSet from "./ServiceSet.svelte";
    import axios from "axios";
    import { api } from "../../stores/api";
    import { config } from "../../lib/scorpion.config";

    let page = 0;

    export let profile_ids = [];

    let service = {
        name: '',
        abbreviation: '',
        provider: '',
        license: '',
        stage: '',
        consortia: [],
        category: '',
        additionalKPI: ''
    };

    // $: console.log(service);

    function validate() {
        if (service.name === '') {
            return false
        }
        if (service.abbreviation === '') {
            return false
        }
        if (service.provider === '') {
            return false
        }
        if (service.category === '') {
            return false
        }
        for (let profile_id of profile_ids) {
            for (let field of config.service_profiles.find((profile) => profile.id === profile_id).fields) {
                if (field.required && service[field.jsonPath] === '') {
                    return false
                }
            }
        }
        return true
    }

    function reset() {
        service = {
            name: '',
            abbreviation: '',
            provider: '',
            license: '',
            stage: '',
            consortia: [],
            category: '',
            additionalKPI: ''
        };
    }

    async function submitForm() {
        console.log(service);
        if (validate()) {
            const response = await axios.post('/bonsai', service, {
                baseURL: $api.base_url + $api.modules.v1
            });
            if (response.status === 200) {
                reset();
            }
        }
    }
</script>

<Card title="Service Registration Form">
    <div slot="card-content">
        {#if page==0}
        <ServiceProfile bind:service bind:profile_ids></ServiceProfile>
        <div class="py-2 flex justify-end">
            <button class="btn btn-sm btn-primary" on:click={()=>{page++}}>{"KPI Set >>"}</button>
        </div>        
        {:else}
        <ServiceSet bind:service/>
        <div class="py-2 flex justify-between">
            <button class="btn btn-sm btn-secondary" on:click={()=>{page--}}>{"<< Service Profile"}</button>
            <button class="btn btn-sm btn-primary" on:click={submitForm}>Submit</button>
        </div>   
        {/if}
    </div>
</Card>