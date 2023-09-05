<script>
	import SignInPrompt from '$lib/components/authentication/SignInPrompt.svelte';
	import './styles.css';
	import { token } from '$lib/stores/api';
	import Header from '$lib/components/Header.svelte';

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
