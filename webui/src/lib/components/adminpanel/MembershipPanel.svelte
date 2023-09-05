<script lang="ts">
  import { UserAvatarFilled } from "carbon-icons-svelte";
  import Card from "../pageContents/Card.svelte";
  import {open_requests, providers, users} from "$lib/stores/admin"
  import axios from "axios";
  import { api } from "$lib/stores/api";

  async function answerRequest(request_id: string, decision: boolean) {
      const response = await axios.delete('/requests/membership', {
          baseURL: $api.base_url+$api.modules.aai,
          params: {
              request_id: request_id,
              accept: decision
          }
      })
      if (response.status===200) {
        let request = $open_requests.find((r)=>{return r.id===request_id})
        if(decision) {
          $users.forEach((u)=>{
            if (request?.username===u.user_name) {
              u.providers = [...u.providers, request.provider]
            }
          })
        }
        $users=$users
        $open_requests = $open_requests.filter((e)=>{return e.id!=request_id})
      }
  }
</script>

<Card title="Service Provider Membership Requests">
    <div slot="card-content">
        <div class="overflow-x-auto">
            <table class="table">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Service Provider</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {#if $open_requests.length===0}
                <tr>
                  There are currently no open requests 
                </tr>
                {/if}
                {#each $open_requests as request}
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
                          <div class="font-bold">{request.username}</div>
                          <div class="text-sm opacity-50">{request.mail}</div>
                        </div>
                      </div>
                    </td>
                    <td>
                        {$providers.find((e)=>{return e.abbreviation===request.provider})?.name}
                        <br>
                        <span class="badge badge-primary">{request.provider}</span>
                    </td>
                    <th class="text-center">
                        <button class="btn btn-ghost hover:btn-success" on:click={()=>{answerRequest(request.id, true)}}>Accept</button>
                        <button class="btn btn-ghost hover:btn-error" on:click={()=>{answerRequest(request.id, false)}}>Decline</button>
                    </th>
                  </tr>
                {/each}
              </tbody>              
            </table>
          </div>
    </div>
</Card>