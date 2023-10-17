<script>
	import SignInPrompt from '$lib/components/authentication/SignInPrompt.svelte';
	import './styles.css';
	import { token } from '$lib/stores/api';
	import Header from '$lib/components/Header.svelte';
	import { onMount } from 'svelte';
	import axios from 'axios';

	onMount(()=>{
		let tmp = localStorage.getItem('token')
		if (tmp) {
			$token=tmp
            axios.defaults.headers.common['Authorization']='Bearer '+$token
		}
	})

</script>

{#if $token.length==0}
	<SignInPrompt/>
{:else}
<div class="app">
	<Header/>
	<main>
		<slot />
	</main>
</div>
{/if}
