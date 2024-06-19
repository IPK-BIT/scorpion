<script lang="ts">
	import { api, token } from '$lib/stores/api';
	import axios from 'axios';
	import RegisterCard from '$lib/components/authentication/RegisterCard.svelte';
	import ResetCard from '$lib/components/authentication/ResetCard.svelte';
	import SignInCard from '$lib/components/authentication/SignInCard.svelte';
	import type { UserAuthentication } from '$lib/stores/types';
	import LsLogin from './LSLogin.svelte';

	let user: UserAuthentication;
	let openError: boolean = false;

	async function tryLogin() {
		try {
			// const response = await axios.post("/login", {}, {
			//     baseURL: $api.base_url+$api.modules.aai,
			//     headers: {
			//         'Authorization': 'Basic '+btoa(user.username+":"+user.password)
			//     }
			// })
			// if (response.status===200) {
			//     token.set(response.data.token)
			//     localStorage.setItem('token', response.data.token)
			//     axios.defaults.headers.common['Authorization']='Bearer '+$token
			//     if (user.remember) {
			//         //TODO implement storing of token in localstorage
			//     }
			// } else {
			//     openError=true;
			// }
			let params = new URLSearchParams();
			params.append('grant_type', 'password');
			params.append('scope', 'openid');
			params.append('username', user.username);
			params.append('password', user.password);
			let api_key = import.meta.env.VITE_API_KEY;
			const response = await axios.post('/token', params, {
				baseURL: $api.base_url + '/realms/scorpion/protocol/openid-connect',
				headers: {
					Authorization: 'Basic ' + api_key,
					'Content-Type': 'application/x-www-form-urlencoded'
				}
			});
			if (response.status === 200) {
				token.set(response.data.access_token);
				localStorage.setItem('token', response.data.access_token);
				axios.defaults.headers.common['Authorization'] = 'Bearer ' + $token;
				if (user.remember) {
					//TODO implement storing of token in localstorage
				}
			} else {
				openError = true;
			}
		} catch {
			openError = true;
		}
	}

	async function tryRegister() {
		if (
			user.password === user.repeat &&
			user.password.length >= 8 &&
			user.email &&
			user.email.length > 0
		) {
			try {
				const response = await axios.post(
					'/register',
					{
						user_name: user.username,
						email: user.email,
						password: user.password
					},
					{
						baseURL: $api.base_url + $api.modules.aai
					}
				);
				context = 'login';
			} catch {}
		} else {
			openError = true;
		}
	}

	async function tryReset() {
		alert('Not yet implemented');
	}

	let context: 'login' | 'register' | 'reset' | 'lslogin' = 'login';
</script>

<svelte:head>
	<title>Scorpion</title>
</svelte:head>

{#if openError}
	<div class="fixed top-0 right-0 z-10 w-full p-4">
		<div class="alert alert-error">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="stroke-current shrink-0 h-6 w-6"
				fill="none"
				viewBox="0 0 24 24"
				><path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
				/></svg
			>
			<span>Error! Task failed successfully.</span>
			<button
				on:click={() => {
					openError = false;
				}}>✕</button
			>
		</div>
	</div>
{/if}
<div
	class="hero min-h-screen bg-neutral bg-cover bg-center"
	style="background-image: url(https://scorpion.bi.denbi.de/scorpion.png);"
>
	<div class="hero-content flex-col lg:flex-row-reverse">
		<div class="text-center lg:text-left text-white">
			<h1 class="text-5xl font-bold">Scorpion</h1>
			<p class="py-6">Service Monitoring KPI Dashboard for NFDI</p>
		</div>
		<!-- {#if context==="reset"}
        <ResetCard 
        on:submit={tryReset} 
        on:loginRequest={()=>{context="login"}}
        on:registerRequest={()=>{context="register"}} 
        />
        {:else if context==="register"}
        <RegisterCard
        bind:user
        on:submit={tryRegister}
        on:loginRequest={()=>{context="login"}}
        />
        {:else if context==="lslogin"}
        <LsLogin/>
        {:else}
        <SignInCard 
        bind:user 
        on:submit={tryLogin} 
        on:registerRequest={()=>{context="register"}} 
        on:resetRequest={()=>{context="reset"}}
        on:lsLoginRequest={()=>{context="lslogin"}}
        />
        {/if} -->
		<LsLogin />
	</div>
</div>
