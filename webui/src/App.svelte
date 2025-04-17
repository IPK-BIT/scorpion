<script>
  import LoginPage from "./components/LoginPage.svelte";
  import Router from "svelte-spa-router";
  import { routes } from "./stores/routes";
  import Header from "./components/Header.svelte";
  import Footer from "./components/Footer.svelte";
  import { token } from "./stores/api";
  import axios from "axios";
    import { onMount } from "svelte";
    import { config } from "./lib/scorpion.config";

  // if (!$token) {
  //   token.set(localStorage.getItem("token"));
  //   axios.defaults.headers.common['Authorization'] = 'Bearer ' + $token;
  // }

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
				redirect_uri: config.domain_name + config.prefix,
				code_verifier: verifier
			};
			let res = await axios.post(`${config.aai.oidc.base_url}/oidc/token`, data, {
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
				const response = await axios.get(`${config.aai.oidc.base_url}/oidc/userinfo`);
			} catch (error) {
				token.set('');
				localStorage.setItem('token', '');
				window.location.href = config.domain_name + config.prefix;
			}
		}
	});
</script>

{#if $token}
<main class="min-h-svh">
  <Header/>
  <Router {routes} />
</main>
<Footer/>
{:else}
<LoginPage/>
{/if}