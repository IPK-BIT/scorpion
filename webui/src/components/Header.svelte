<script>
    import { Menu, UserProfile, WarningAlt } from "carbon-icons-svelte";
    import { api, token } from "../stores/api"; 
    import axios from "axios";
    import { config } from "../lib/scorpion.config";

    function logout() {
        token.set(null);
        localStorage.removeItem("token");
        window.location.href = config.domain_name + config.prefix;
    }

    async function collectNotification() {
      const response = await axios('/notification', {
        baseURL: $api.base_url + $api.modules.v1
      })
      return response.data;
    }
</script>

<div class="p-2 mb-2 shadow-md bg-primary text-primary-content flex flex-row">
    <div class="flex flex-row space-x-2 items-center">
        <button class="btn btn-ghost btn-sm" popovertarget="popover-1" style="anchor-name:--anchor-1">
            <Menu class="w-6 h-6" />
          </button>
          <ul class="dropdown menu w-52 rounded-box bg-base-100 shadow-sm"
            popover="auto" id="popover-1" style="position-anchor:--anchor-1">
            <li><a class="text-base-content" href="#/">Dashboard</a></li>
            <li><a class="text-base-content" href="#/register">Service Registration</a></li>
            <li><a class="text-base-content" href="#/submit">KPI Submission</a></li>
            <li><a class="text-base-content hover:bg-warning" href="#/admin">Administration</a></li>
          </ul>
        <div class="flex flex-row items-center">
            <img class="w-10 h-10" src={config.prefix+"/scorpion-transparent.png"} alt="scorpion" />
            <h1 class="text-xl">Scorpion</h1>
        </div>
    </div>
    <div class="ml-auto flex items-center px-2">
        <button class="btn btn-outline btn-circle btn-sm" popovertarget="popover-2" style="anchor-name:--anchor-2">
            <UserProfile class="w-6 h-6 m-1" />
          </button>
          <ul class="dropdown dropdown-end menu w-52 rounded-box bg-base-100 shadow-sm"
            popover="auto" id="popover-2" style="position-anchor:--anchor-2">
            <li><a class="text-base-content" href="#/profile">Profile</a></li>
            <li><a class="text-base-content" href={config.prefix+"/docs"}>API Docs</a></li>
            <li><button class="text-base-content hover:bg-error" on:click={logout}>Logout</button></li>
          </ul>
    </div>
</div>
{#await collectNotification()}
<div role="alert" class="alert alert-info mb-2 mx-1">
<span>Loading...</span>
</div>
{:then notification} 
<div role="alert" class="alert alert-warning mb-2 mx-1">
  <WarningAlt class="w-6 h-6" />
  <span>
  {@html notification}
  </span>
</div>
{/await}

