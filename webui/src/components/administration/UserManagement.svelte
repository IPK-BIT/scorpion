<script>
	import { Close, UserAvatarFilled } from 'carbon-icons-svelte';
	import axios from 'axios';
	import { api } from '../../stores/api';
    import { onMount } from 'svelte';

    let open_requests = [];
    let users = [];
    let providers = [];
    let selectedUser;
    let editMode = false;
    let changes = false;

    let user_providers = [];

    async function answerRequest(request_id, decision) {
		const response = await axios.delete('/requests/membership', {
			baseURL: $api.base_url + $api.modules.aai,
			params: {
				request_id: request_id,
				accept: decision
			}
		});
		if (response.status === 200) {
			let request = open_requests.find((r) => {
				return r.id === request_id;
			});
			if (decision) {
				users.forEach((u) => {
					if (request?.username === u.user_name) {
						u.providers = [...u.providers, request.provider];
					}
				});
			}
			users = users;
			open_requests = open_requests.filter((e) => {
				return e.id != request_id;
			});
		}
	}

    function selectUser(user) {
        user_providers = [];
        selectedUser = user;
        for (let provider of user.providers) {
            user_providers = [...user_providers, {'name': provider, 'checked': true}];
        }
    }

    async function sendUpdate() {
        let user = selectedUser;
        user.providers = user_providers.filter((p)=>p.checked).map((p)=>p.name);

        const response = await axios.put('/users', user, {
            baseURL: $api.base_url + $api.modules.aai
        });
        if (response.status === 200) {
            users = users.map((u) => {
                if (u.user_name === user.user_name) {
                    return user;
                }
                return u;
            });
            selectedUser = null;
            user_providers = [];
            editMode = false;
            changes = false;
        }
    }

    onMount(async () => {
        let response = await axios.get(`${$api.base_url}${$api.modules.aai}/users`);
        users = response.data;

        response = await axios.get(`${$api.base_url}${$api.modules.aai}/requests/membership`);
        open_requests = response.data;

        response = await axios.get(`${$api.base_url}${$api.modules.v1}/providers`);
        providers = response.data.result;
    });
</script>
<div class="flex flex-row space-x-2">
    <div class="{selectedUser?'w-2/3':'w-full'}">
    <table class="table">
        <thead>
            <tr>
                <th>Name</th>
                <th>Service Providers</th>
                <th>Role</th>
            </tr>        
        </thead>
        <tbody>
            {#each users as user}
            <tr class="hover:bg-base-200 cursor-pointer" on:click={()=>selectUser(user)}>
                <td>
                    <div class="flex items-center space-x-3">
                        <div class="avatar">
                            <div class="mask mask-squircle w-12 h-12">
                                <svg class="w-12 h-12" viewBox="0 0 24 24">
                                    <UserAvatarFilled size={24} />
                                </svg>
                            </div>
                        </div>
                        <div>
                            <div class="font-bold space-x-1">
                                <span>{user.user_name}</span>
                                {#if open_requests.filter((req)=>req.mail==user.email).length > 0}
                                <div class="status status-info animate-bounce"></div>
                                {/if}
                            </div>
                            <div class="text-sm opacity-50">{user.email}</div>
                        </div>
                    </div>
                </td>
                <td>
                    {#each user.providers as provider}
                        <span class="badge badge-primary m-1">{provider}</span>
                    {/each}
                </td>
                <td>
                    {#if user.is_admin}
                        <span class="badge badge-accent">Administrator</span>
                    {:else}
                        <span class="badge badge-secondary">User</span>
                    {/if}
                </td>
            </tr>
            {/each}
        </tbody>
    </table>
    </div>
    {#if selectedUser}
    <div class="border border-base-300 w-1/3 h-[calc(100vh-4rem)] bg-white rounded-box shadow-2xl">
        <div class="relative top-2 right-2 w-full flex justify-end p-2">
            <button class="btn btn-ghost btn-circle" on:click={()=>{selectedUser=null;editMode=false;}}><Close size={24}/></button>
        </div>
        <div class="p-4">
            <div class="flex flex-col items-center">
                <div class="avatar">
                    <div class="mask mask-squircle w-24 h-24">
                        <svg class="w-24 h-24" viewBox="0 0 24 24">
                            <UserAvatarFilled size={24} />
                        </svg>
                    </div>
                </div>
                <div class="flex flex-col items-center">
                    <div class="font-bold">{selectedUser.user_name}</div>
                    <div class="text-sm opacity-50">{selectedUser.email}</div>
                </div>
            </div>
            <div class="divider">
                <label class="swap swap-flip">
                    <input type="checkbox" bind:checked={editMode}/>
                    <div class="swap-off">
                        <div class="badge badge-secondary">
                            <span>Edit User</span>
                            <pre>OFF</pre>
                        </div>
                    </div>
                    <div class="swap-on">
                        <div class="badge badge-primary">
                            <span>Edit User</span>
                            <pre>ON</pre>
                        </div>
                    </div>    
                </label>                    
            </div>
            <fieldset class="mt-4 fieldset bg-base-100 border border-base-300 p-4 rounded-box">
                <legend class="fieldset-legend">Service Providers</legend>
                <ul class="space-y-2">
                    {#each user_providers as provider}
                    <li class="flex justify-between">
                        <span>{providers.find((p)=>p.abbreviation===provider.name).name}</span>
                        <input disabled={!editMode} type="checkbox" class="checkbox" bind:checked={provider.checked} on:change={()=>{changes=true}}/>
                    </li>
                    {/each}
                    {#each open_requests.filter((req)=>req.user==selectedUser.name) as req}
                    <li class="flex justify-between">
                        <span>{providers.find((p)=>p.abbreviation === req.provider).name}</span>
                        <div class="flex flex-row space-x-2">
                            <button class="btn btn-ghost btn-sm hover:btn-success uppercase" on:click={()=>answerRequest(req.id, true)}>Approve</button>
                            <button class="btn btn-ghost btn-sm hover:btn-error uppercase" on:click={()=>answerRequest(req.id, false)}>Decline</button>
                        </div>
                    </li>                        
                    {/each}
                </ul>
            </fieldset>
            <fieldset class="mt-2 fieldset bg-base-100 border border-base-300 p-4 rounded-box">
                <legend class="fieldset-legend">Roles</legend>
                <ul class="space-y-2">    
                    <li class="flex flex-row justify-between">
                        <span>User</span>
                        <input disabled type="checkbox" class="checkbox" checked/>
                    </li>
                    <li class="flex flex-row justify-between">
                        <span>Administrator</span>
                        <input disabled={!editMode} type="checkbox" class="checkbox" bind:checked={selectedUser.is_admin} on:change={()=>{changes=true}}/>
                    </li>
                </ul>
            </fieldset>
            {#if editMode}
            <div class="p-1 mt-2">
                <button disabled={!changes} class="uppercase btn btn-primary w-full" on:click={sendUpdate}>Submit Changes</button>
            </div>
            {/if}
        </div>        
    </div>
    {/if}
</div>