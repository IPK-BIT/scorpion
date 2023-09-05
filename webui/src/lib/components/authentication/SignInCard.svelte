<script lang="ts">
	import { token } from "$lib/stores/api";
	import type { UserAuthentication } from "$lib/stores/types";
	import { createEventDispatcher } from "svelte";

    export const user: UserAuthentication = {
        username: "",
        password: "",
        remember: true
    }

    const dispatch = createEventDispatcher();
    function sendRegister() {dispatch('registerRequest', {})}
    function sendReset() {dispatch('resetRequest', {})}
</script>

<div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
    <form class="card-body" on:submit>
        <div class="form-control">
            <label for="email" class="label">
                <span class="label-text">Email</span>
            </label>
            <input id="email" type="text" placeholder="Enter email or username" class="input input-bordered" bind:value={user.username}/>
        </div>
        <div class="form-control">
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label for="password" class="label">
                <span class="label-text">Password</span>
            </label>
            <input id="password" type="password" placeholder="Enter password" class="input input-bordered" bind:value={user.password}/>
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="label">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-missing-attribute -->
                <a class="label-text-alt link link-hover" on:click={sendRegister}>Register</a>
                <!-- svelte-ignore a11y-missing-attribute -->
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!--<a class="label-text-alt link link-hover" on:click={sendReset}>Forgot password?</a>-->
            </label>
        </div>
        <div class="form-control">
            <label class="label cursor-pointer">
                <span class="label-text text-sm">Remember me</span> 
                <input type="checkbox" class="toggle toggle-sm" checked bind:value={user.remember}/>
            </label>
        </div>
        <div class="form-control mt-1">
            <input type="submit" value="Login" class="btn btn-primary"/>
        </div>
    </form>
</div>