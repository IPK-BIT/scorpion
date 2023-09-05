<script lang="ts">
	import type { MembershipRequest, ServiceProvider, UserDetail } from "$lib/stores/types";
	import { Add, Close } from "carbon-icons-svelte";
    import Card from "../pageContents/Card.svelte";
	import { api } from "$lib/stores/api";
	import axios from "axios";

    let selected_provider: string = "";

    async function requestMembership() {
        const response = await axios.post('/requests/membership',{}, {
            baseURL: $api.base_url+$api.modules.aai,
            params: {providers: selected_provider}
        })
        if (response.status===201) {
            openRequests= [...openRequests, ...[{id: "", mail: "", username: "", provider: selected_provider}]]
            selected_provider=""
        }
    }

    export let providers: ServiceProvider[]
    export let details: UserDetail;
    export let openRequests: MembershipRequest[];
</script>

<div class="flex flex-col p-4 space-y-4">
    <Card title="User Information">
        <div slot="card-content" class="form-control space-y-4">
            <div class="space-y-2">
                <label class="input-group">
                    <span class="w-1/12 label-text">Username</span> 
                    <input type="text" disabled class="w-11/12 input input-bordered" bind:value={details.user_name}/>
                </label>
                <label class="input-group">
                    <span class="w-1/12 label-text">Email</span> 
                    <input type="text" disabled class="w-11/12 input input-bordered" bind:value={details.email}/>
                </label>
            </div>
            <div class="divider">Roles</div>
            <label class="label cursor-pointer">
                <span class="label-text">Admin</span> 
                <input type="checkbox" disabled bind:checked={details.is_admin} class="checkbox" />
            </label>
            <div class="divider">
                Service Provider Memberships
                <button class="btn btn-circle btn-accent btn-sm" onclick="my_modal_3.showModal()"><Add/></button>
            </div>
            {#each details.providers as provider}
            <label class="label cursor-pointer">
                <span class="label-text">{provider}</span> 
                <input type="checkbox" disabled checked class="checkbox" />
            </label>
            {/each}
            {#each openRequests as request}
            <label class="label cursor-pointer">
                <span class="label-text text-gray-200">{request.provider}</span> 
                <input type="checkbox" disabled class="checkbox" />
            </label>
            {/each}
        </div>
    </Card>
</div>

<dialog id="my_modal_3" class="modal">
  <form method="dialog" class="modal-box">
    <button class="btn btn-circle btn-ghost absolute right-2 top-2"><Close size={32}/></button>
    <h3 class="font-bold text-lg">Request Membership</h3>
    <div class="join w-full py-2">
        <label for="provider" class="join-item bg-base-300 label label-text w-[30%]">Service Provider</label>
        <select id="provider" class="join-item select select-bordered w-[70%]" bind:value={selected_provider}>
            <option disabled selected value="">Select a Service Provider</option>
            {#each providers as provider}
                <option value={provider.abbreviation}>{provider.name}</option>
            {/each}
        </select>
    </div>
    <div class="flex justify-end">
        <button class="btn btn-secondary" on:click={requestMembership}>Request Membership</button>
    </div>
  </form>
</dialog>