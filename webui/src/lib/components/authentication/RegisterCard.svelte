<script lang="ts">
	import type { UserAuthentication } from "$lib/stores/types";
	import { createEventDispatcher } from "svelte";

    export const user: UserAuthentication = {
        username: "",
        email: "",
        password: "",
        repeat: ""
    }

    const dispatch = createEventDispatcher();
    function sendLogin() {dispatch('loginRequest', {})}
</script>

<div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
    <form class="card-body" on:submit>
        <div class="form-control">
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="label">
                <span class="label-text">Username</span>
            </label>
            <input type="text" placeholder="Enter username" class="input input-bordered" bind:value={user.username}/>
        </div>
        <div class="form-control">
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="label">
                <span class="label-text">Email</span>
            </label>
            <input type="text" placeholder="Enter email" class="input input-bordered" bind:value={user.email}/>
        </div>
        <div class="form-control">
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="label">
                <span class="label-text">Password</span>
            </label>
            <input type="password" placeholder="Enter password" class="input input-bordered" bind:value={user.password}/>
        </div>
        <div class="form-control">
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="label">
                <span class="label-text">Repeat password</span>
            </label>
            <input type="password" placeholder="Repeat password" class="input input-bordered" bind:value={user.repeat}/>
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="label">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-missing-attribute -->
                <a class="label-text-alt link link-hover" on:click={sendLogin}>Sign in</a>
            </label>
        </div>
        <div class="form-control mt-6">
            <input type="submit" value="Register" class="btn btn-primary"/>
        </div>
    </form>
</div>