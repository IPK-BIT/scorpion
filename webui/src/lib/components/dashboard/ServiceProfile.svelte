<script lang="ts">
	import type { Metadata, Service } from "$lib/stores/types";
	import { Edit, EditOff, Locked, Unlocked } from "carbon-icons-svelte";
	import DocumentationForm from "../bonsai/forms/DocumentationForm.svelte";
	import GeneralInformationForm from "../bonsai/forms/GeneralInformationForm.svelte";
	import OrganizationalInformationForm from "../bonsai/forms/OrganizationalInformationForm.svelte";
	import ReportingForm from "../bonsai/forms/ReportingForm.svelte";
	import SupportForm from "../bonsai/forms/SupportForm.svelte";
	import TechnicalInfrastructureForm from "../bonsai/forms/TechnicalInfrastructureForm.svelte";
	import Card from "../pageContents/Card.svelte";
	import axios from "axios";
	import { api } from "$lib/stores/api";

    export let services: Service[] = [];

    let selected = "";

    let metadata:Metadata = {
                name: "",
                abbreviation: "",
                provider: "",
                areaofapplication: {
                    planning: false,
                    harmonization: false,
                    access: false,
                    discover: false,
                    processing: false,
                    support: false
                },
                description: "",
                inputformats: "",
                outputformats: "",
                developmentstage: "",
                version: "",
                documentation: "",
                license: "",
                link: "",
                serviceorientation: "",
                includeincataglog: "",
                serviceprovidedas: {
                    institutionalMission: {
                        partOf: false,
                        percentage: 0
                    },projectFunding: {
                        partOf: false,
                        percentage: 0
                    },others: {
                        partOf: false,
                        percentage: 0
                    }
                },
                funding: "",
                contact: "",
                helpdesk: "",
                supporteduntil: "",
                technicalbackbone: "",
                disasterplan: "",
                entrancecontrol: "",
                operationstability: "",
                templates: "",
                communication: "",
                registered: {
                    biotools: {
                        registered: false,
                        url: ""
                    },risources: {
                        registered: false,
                        url: ""
                    },eosc: {
                        registered: false,
                        url: ""
                    },fairsharing: {
                        registered: false,
                        url: ""
                    },re3data: {
                        registered: false,
                        url: ""
                    },others: {
                        registered: false,
                        url: ""
                    },
                },
                publications: "",
                category: "",
                additionalKPI: []
            };

    async function loadProfile() {
        const response = await axios.get('/services', {
            baseURL: $api.base_url+$api.modules.v1,
            params: {
                service: selected,
            }
        })
        if (response.status===200) {
            console.log(response.data)
            metadata=response.data[0]
        }
    }

    let active = 0;
</script>

<Card title="Service Profile">
    <div slot="card-content" class="space-y-2">
        <div class="flex flew-row space-x-4 ">
            <select class="select select-bordered w-full" bind:value={selected} on:change={loadProfile}>
                <option value="" disabled selected>Pick one</option>
                {#each services as service}
                    <option value={service.abbreviation}>{service.name}</option>
                {/each}
            </select>
            <!--<div class="flex justify-end">
                <label class="swap">
                    <input type="checkbox" />
                    <Edit class="swap-on w-8 h-8 text-gray-500" size={24}/>
                    <EditOff class="swap-off w-8 h-8 text-gray-400" size={24}/>
                  </label>
            </div>-->
        </div>
        {#if selected.length>0}
        <div class="tabs tabs-boxed flex justify-center">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <btn class="tab {active===0?"tab-active":""}" on:click={()=>{active=0}}>General Information</btn> 
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <btn class="tab {active===1?"tab-active":""}" on:click={()=>{active=1}}>Organizational Information</btn> 
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <btn class="tab {active===2?"tab-active":""}" on:click={()=>{active=2}}>Support</btn>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <btn class="tab {active===3?"tab-active":""}" on:click={()=>{active=3}}>Technical Infrastructure</btn>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <btn class="tab {active===4?"tab-active":""}" on:click={()=>{active=4}}>Documentation</btn>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <btn class="tab {active===5?"tab-active":""}" on:click={()=>{active=5}}>Reporting</btn>
        </div>
        <div>
            {#if active===0}
            <GeneralInformationForm bind:metadata/>
            {:else if active===1}
            <OrganizationalInformationForm bind:metadata/>
            {:else if active===2}
            <SupportForm bind:metadata/>
            {:else if active===3}
            <TechnicalInfrastructureForm bind:metadata/>
            {:else if active===4}
            <DocumentationForm bind:metadata/>
            {:else if active===5}
            <ReportingForm bind:metadata/>
            {/if}
        </div>
        {/if}
    </div>
</Card>