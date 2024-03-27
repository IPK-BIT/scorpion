<script lang="ts">
	import KpiView from "$lib/components/adminpanel/KPIView.svelte";
    import ReportView from "$lib/components/adminpanel/ReportView.svelte";
	import ResultView from "$lib/components/adminpanel/ResultView.svelte";
	import UserView from "$lib/components/adminpanel/UserView.svelte";
	import Unauthorized from "$lib/components/pageContents/Unauthorized.svelte";
    import { api, token } from "$lib/stores/api";
	import type { UserDetail } from "$lib/stores/types";
	import axios from "axios";
	import { ChartLineData, DataClass, Group, Report } from "carbon-icons-svelte";
	import { onMount } from "svelte";
    import { jwtDecode } from "jwt-decode";

    let details: UserDetail;
    let context: string = "";
    onMount(async ()=>{
        // const response = await axios.get('/details', {
        //     baseURL: $api.base_url+$api.modules.aai
        // })
        // if (response.status===200) {
        //     details = response.data
        // }
        // const response = await axios.get('/userinfo', {
        //     baseURL: $api.base_url+'/realms/scorpion/protocol/openid-connect'
        // })
        // if (response.status===200) {
        //     console.log(response.data)
        // }

        const jwtToken = $token;
        if (jwtToken) {
            const decodedToken = jwtDecode(jwtToken);
            details = {
                user_name: decodedToken.preferred_username,
                email: decodedToken.email,
                is_admin: decodedToken.realm_access.roles.includes("admin"),
                providers: [],
            }
            
        }
    })
</script>

<svelte:head>
<title>Admin Panel</title>
<meta name="description" content="Administration Page" />
<script src="https://cdn.plot.ly/plotly-latest.min.js" type="text/javascript"></script>	
</svelte:head>

{#if details && details.is_admin}
    <div class="text-lg font-bold breadcrumbs p-4">
        <ul>
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-missing-attribute -->
        <li><a on:click={()=>{context=""}}>Administration</a></li> 
        {#if context==="users"}
        <li>Users</li> 
        {:else if context==="results"}
        <li>Results</li> 
        {:else if context==="kpis"}
        <li>KPIs</li> 
        {:else if context==="report"}
        <li>Report Cards</li> 
        {/if}
        </ul>
    </div>
{#if context===""}
<div class="flex flex-row space-x-8 justify-center p-4">
    <div class="card bg-white shadow-xl w-72">
        <figure class="px-10 pt-10">
            <svg class="h-16 w-16" viewBox="0 0 16 16"><Group size={16}/></svg>
        </figure>
        <div class="card-body items-center">
            <h2 class="card-title">User Administration</h2>
            <p>You find all tools related to user permission & access management here!</p>
            <div class="card-actions">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <btn class="btn btn-primary" on:click={()=>{context="users"}}>Visit</btn>
            </div>
        </div>
    </div>    
    <div class="card bg-white shadow-xl w-72">
        <figure class="px-10 pt-10">
            <svg class="h-16 w-16" viewBox="0 0 16 16"><DataClass size={16}/></svg>
        </figure>
        <div class="card-body items-center">
            <h2 class="card-title">KPIs Administration</h2>
            <p>You find all tools related to Service Categories & KPIs here!</p>
            <div class="card-actions">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <btn class="btn btn-primary" on:click={()=>{context="kpis"}}>Visit</btn>
            </div>
        </div>
    </div>    
    <div class="card bg-white shadow-xl w-72">
        <figure class="px-10 pt-10">
            <svg class="h-16 w-16" viewBox="0 0 16 16"><ChartLineData size={16}/></svg>
        </figure>
        <div class="card-body items-center">
            <h2 class="card-title">Results Administration</h2>
            <p>You find all tools related to measurements here!</p>
            <div class="card-actions">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <btn class="btn btn-primary" on:click={()=>{context="results"}}>Visit</btn>
            </div>
        </div>
    </div>
    <div class="card bg-white shadow-xl w-72">
        <figure class="px-10 pt-10">
            <svg class="h-16 w-16" viewBox="0 0 16 16"><Report size={16}/></svg>
        </figure>
        <div class="card-body items-center">
            <h2 class="card-title">Report Card</h2>
            <p>You find all tools related to user permission & access management here!</p>
            <div class="card-actions">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <btn class="btn btn-primary" on:click={()=>{context="report"}}>Visit</btn>
            </div>
        </div>
    </div>
</div>
{:else if context==="users"}
<UserView/>
{:else if context==="results"}
<ResultView/>
{:else if context==="kpis"}
<KpiView/>
{:else if context==="report"}
<ReportView/>
{/if}
{:else}
<Unauthorized/>
{/if}