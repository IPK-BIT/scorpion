<script>
	import SignInPrompt from '$lib/components/authentication/SignInPrompt.svelte';
	import './styles.css';
	import { token } from '$lib/stores/api';
	import Header from '$lib/components/Header.svelte';
	import { onMount } from 'svelte';
	import axios from 'axios';
	import { goto } from '$app/navigation';
	import { PUBLIC_ENVIRONMENT, PUBLIC_OIDC_URL, PUBLIC_DOMAIN_NAME } from '$env/static/public';

	onMount(async () => {
		// get URL search params
		let url = new URL(window.location.href);
		let params = url.searchParams;
		let code = params.get('code');
		if (code) {
			let verifier = localStorage.getItem('codeVerifier');
			let data = {
				grant_type: 'authorization_code',
				code: code,
				client_id: 'aa30af02-f470-4508-880e-8f8c99652143',
				redirect_uri: PUBLIC_DOMAIN_NAME,
				code_verifier: verifier
			};
			let res = await axios.post(`${PUBLIC_OIDC_URL}/oidc/token`, data, {
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded'
				}
			});
			$token = res.data.access_token;
			localStorage.setItem('token', $token);
			// remove searchParams from URL
			window.history.replaceState({}, document.title, window.location.pathname);

			axios.defaults.headers.common['Authorization'] = 'Bearer ' + $token;
		}

		let tmp = localStorage.getItem('token');
		if (tmp) {
			$token = tmp;
			axios.defaults.headers.common['Authorization'] = 'Bearer ' + $token;
			try {
				const response = await axios.get(`${PUBLIC_OIDC_URL}/oidc/userinfo`);
			} catch (error) {
				token.set('');
				localStorage.setItem('token', '');
				goto('/');
			}
		}
	});
</script>

{#if $token.length == 0}
	<SignInPrompt />
{:else}
	<div class="app">
		<Header />
		{#if PUBLIC_ENVIRONMENT==='dev'||PUBLIC_ENVIRONMENT==='test'}
		<div class="p-2">
		<div role="alert" class="alert alert-error">
			<svg
			  xmlns="http://www.w3.org/2000/svg"
			  class="h-6 w-6 shrink-0 stroke-current"
			  fill="none"
			  viewBox="0 0 24 24">
			  <path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
			</svg>
			{#if PUBLIC_ENVIRONMENT==='dev'}
			<span>Warning: Development Instance. There are no backups made and data can be deleted without further notice!</span>
			{:else}
			<span>Warning: Test Instance. There are no backups made and data can be deleted without further notice!</span>
			{/if}
		  </div>
		</div>
		{/if}
		<main>
			<slot />
		</main>
	</div>
{/if}
