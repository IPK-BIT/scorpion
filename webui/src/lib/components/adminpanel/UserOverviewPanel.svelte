<script lang="ts">
    import { Close, TrashCan, UpdateNow, UserAvatarFilled } from "carbon-icons-svelte";
    import Card from "../pageContents/Card.svelte";
    import type { UserDetail } from "$lib/stores/types";
	import axios from "axios";
	import { api } from "$lib/stores/api";
	import { open_requests, users } from "$lib/stores/admin";
    
    let selected_user: UserDetail = {
        user_name: "feserm",
        email: "feser@ipk-gatersleben.de",
        is_admin: true,
        providers: ["IPK"]
    }
    
    let selected_providers: boolean[] = [];
    
    function copyUser(user: UserDetail) {
        selected_providers=[];
        selected_user = {
            user_name: user.user_name, 
            email: user.email, 
            is_admin: user.is_admin, 
            providers: user.providers
        }
        selected_user.providers.forEach(()=>{selected_providers.push(true)})
    }
    
    async function sendUpdate() {
        let tmp: string[] =[];
        for (let i=0; i<selected_providers.length; i++) {
            if(selected_providers[i]===true) {
                tmp.push(selected_user.providers[i])
            }
        }
        selected_user.providers=tmp
        const resp = await axios.put('/users', selected_user, {
            baseURL: $api.base_url+$api.modules.aai
        })
        if (resp.status===200) {
            $users.forEach((u)=>{
                if(u.user_name===resp.data.user_name) {
                    u.is_admin=resp.data.is_admin;
                    u.providers=resp.data.providers;
                }
            })
            $users = $users
        }
    }

    async function sendDelete(user_name: string) {
        const resp = await axios.delete('/users', {
            baseURL: $api.base_url+$api.modules.aai,
            params: {
                user_name: user_name
            }
        })
        if(resp.status===200) {
            $open_requests = $open_requests.filter((r)=>{
                return r.username!=user_name
            })
            $users = $users.filter((u)=>{
                return u.user_name!=resp.data.user_name
            })
        }
    }
</script>

<Card title="User Overview">
    <div slot="card-content">
        <div class="">
            <table class="table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Service Providers</th>
                        <th>Role</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {#each $users as user}
                    <tr>
                        <td>
                            <div class="flex items-center space-x-3">
                                <div class="avatar">
                                    <div class="mask mask-squircle w-12 h-12">
                                        <svg class="w-12 h-12" viewBox="0 0 24 24">
                                            <UserAvatarFilled size={24}/>
                                        </svg>
                                    </div>
                                </div>
                                <div>
                                    <div class="font-bold">{user.user_name}</div>
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
                        <th>
                            <div class="dropdown dropdown-hover dropdown-start dropdown-left">
                                <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
                                <!-- svelte-ignore a11y-label-has-associated-control -->
                                <label tabindex="0" class="btn btn-sm btn-ghost m-1">Actions</label>
                                <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
                                <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52 ">
                                    <li><button class="btn btn-ghost btn-sm hover:btn-warning" onclick="my_modal_3.showModal()" on:click={()=>copyUser(user)}>Update <UpdateNow/></button></li>
                                    <li><button class="btn btn-ghost btn-sm hover:btn-error" on:click={()=>{sendDelete(user.user_name)}}>Remove <TrashCan/></button></li>
                                </ul>
                            </div>
                        </th>
                    </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </div>
</Card>

<dialog id="my_modal_3" class="modal">
    <form method="dialog" class="modal-box">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"><Close size={24}/></button>
        <h3 class="font-bold text-lg">Update User Information</h3>
        <form class="space-y-2 py-4">
            <div class="form-control">
                <div class="flex flex-row space-x-4 justify-center">
                    <div class="avatar">
                        <div class="mask mask-squircle w-12 h-12">
                            <svg class="w-12 h-12" viewBox="0 0 24 24">
                                <UserAvatarFilled size={24}/>
                            </svg>
                        </div>
                    </div>
                    <div>
                        <div class="font-bold">{selected_user.user_name}</div>
                        <div class="text-sm opacity-50">{selected_user.email}</div>
                    </div>
                </div>
                <div class="divider">Role</div>
                <label class="label cursor-pointer">
                    <span class="label-text bg-base-100">Administrator</span> 
                    <input type="checkbox" class="checkbox" bind:checked={selected_user.is_admin} />
                </label>
                {#if selected_user.providers.length>0}    
                <div class="divider">Service Provider Memberships</div>
                {#each selected_user.providers as provider, i}
                <label class="label cursor-pointer">
                    <span class="label-text bg-base-100">{provider}</span> 
                    <input type="checkbox" class="checkbox" bind:checked={selected_providers[i]} />
                </label>
                {/each}
                {/if}
            </div>
        </form>
        <div class="flex justify-end">
            <button class="btn btn-primary" on:click={sendUpdate}>Confirm</button>
        </div>
    </form>
</dialog>