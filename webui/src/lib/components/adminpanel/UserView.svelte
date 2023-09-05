<script lang="ts">
	import { onMount } from "svelte";
	import axios from "axios";
	import { api } from "$lib/stores/api";
	import { open_requests, providers, registration_requests, users } from "$lib/stores/admin";
	import MembershipPanel from "./MembershipPanel.svelte";
	import RegistrationPanel from "./RegistrationPanel.svelte";
	import UserOverviewPanel from "./UserOverviewPanel.svelte";

    onMount(async ()=>{
        let response = await axios.get('/providers', {
            baseURL: $api.base_url+$api.modules.v1
        })
        if (response.status===200) {
            providers.set(response.data.result)
        }
        response = await axios.get('/requests/membership', {
            baseURL: $api.base_url+$api.modules.aai
        })
        if (response.status===200) {
            open_requests.set(response.data)
        }
        response = await axios.get('/requests/registration', {
            baseURL: $api.base_url+$api.modules.aai
        })
        if (response.status===200) {
            registration_requests.set(response.data)
            $registration_requests.forEach((r)=>{
                r.is_admin=false
            })
        }
        response = await axios.get('/users', {
            baseURL: $api.base_url+$api.modules.aai
        })
        if (response.status===200) {
            users.set(response.data)
        }
    })
</script>

<div class="p-4 space-y-2">
    <div class="flex flex-row space-x-2">
        <RegistrationPanel/>
        <UserOverviewPanel/>
    </div>
    <div class="flex flex-row space-x-2">
        <MembershipPanel/>
    </div>
</div>