<script>
    import { onMount } from "svelte";
    import UserManagement from "../components/administration/UserManagement.svelte";
    import axios from "axios";
    import { api } from "../stores/api";
    import Card from "../components/Card.svelte";
    import KpiManagement from "../components/administration/KPIManagement.svelte";
    import Measurement from "../components/administration/Measurement.svelte";
    import Evaluation from "../components/administration/Evaluation.svelte";

    let activeTab = 0;

    let is_admin = false;
    onMount(async ()=>{
        const response = await axios.get(`${$api.base_url}${$api.modules.aai}/details`);
        is_admin = response.data.is_admin;
    })

</script>

{#if is_admin}
<div class="flex flex-row px-2">
    <div class="w-1/5 h-[calc(100vh-4rem)] bg-base-200 p-2 rounded-box mb-2">
        <ul class="menu w-full">
            <li class={activeTab === 0 ? 'bg-accent border border-base-300 rounded-lg text-accent-content' : ''}><button on:click={() => activeTab = 0}>Users</button></li>
            <li class={activeTab === 1 ? 'bg-accent border border-base-300 rounded-lg text-accent-content' : ''}><button on:click={() => activeTab = 1}>Key Performance Indicators</button></li>
            <li class={activeTab === 2 ? 'bg-accent border border-base-300 rounded-lg text-accent-content' : ''} ><button on:click={() => activeTab = 2}>Measurements</button></li>
            <li class={activeTab === 3 ? 'bg-accent border border-base-300 rounded-lg text-accent-content' : ''}><button on:click={() => activeTab = 3}>Evaluation</button></li>
        </ul>
    </div>
    <div class="w-4/5 px-4">
        {#if activeTab === 0}
            <UserManagement/>
        {:else if activeTab === 1}
            <KpiManagement/>
        {:else if activeTab === 2}
            <Measurement/>
        {:else if activeTab === 3}
            <Evaluation/>
        {/if}
    </div>
</div>
{:else}
<div class="w-1/2 mx-auto">
    <Card>
        <div slot="card-content">
            <div>
                <h1 class="text-5xl text-primary">401 - Unauthorized</h1>
                <p class="py-2">You are not authorized to access this page.</p>
            </div>
            <a class="btn btn-primary w-full" href="/">Go back</a>
        </div>
    </Card>
</div>
{/if}