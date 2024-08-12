<script>
	import SignInPrompt from '$lib/components/authentication/SignInPrompt.svelte';
	import './styles.css';
	import { token } from '$lib/stores/api';
	import Header from '$lib/components/Header.svelte';
	import { onMount } from 'svelte';
	import axios from 'axios';
	import { goto } from '$app/navigation';

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
				redirect_uri: 'http://192.168.0.64:3000',
				code_verifier: verifier
			};
			let res = await axios.post('http://192.168.0.64:5000/oidc/token', data, {
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
				const response = await axios.get('http://192.168.0.64:5000/oidc/userinfo');
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
		<main>
			<slot />
		</main>
	</div>
{/if}
