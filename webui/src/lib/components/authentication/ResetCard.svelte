<script lang="ts">
	import { createEventDispatcher } from "svelte";

    export let email: string = "";

    const dispatch = createEventDispatcher();
    function sendLogin(){dispatch('loginRequest')}
    function sendRegister(){dispatch('registerRequest')}
</script>

<div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
    <form class="card-body" on:submit>
        <div class="form-control">
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="label">
                <span class="label-text">Email</span>
            </label>
            <input type="text" placeholder="Enter email" class="input input-bordered" bind:value={email}/>
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="label">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-missing-attribute -->
                <a class="label-text-alt link link-hover" on:click={sendLogin}>Sign In</a>
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-missing-attribute -->
                <a class="label-text-alt link link-hover" on:click={sendRegister}>Register</a>
            </label>
        </div>
        <div class="form-control mt-1">
            <input type="submit" value="Send Password Reset" class="btn btn-primary"/>
        </div>
    </form>
</div>