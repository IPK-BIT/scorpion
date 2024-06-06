<script>
    import { onMount } from 'svelte';
    import image from "$lib/assets/button-ls-login.svg"

    function generateCodeVerifier() {
        let codeVerifier = btoa(String.fromCharCode.apply(null, Array.from(globalThis.crypto.getRandomValues(new Uint8Array(32)))));
        codeVerifier = codeVerifier.replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
        return codeVerifier;
    }

    /**
	 * @param {string} codeVerifier
	 */
    async function generateCodeChallenge(codeVerifier) {
        // ASCII codeverifier
        const ascii = new TextEncoder().encode(codeVerifier);
        // Hash codeverifier
        const hashBuffer = await globalThis.crypto.subtle.digest('SHA-256', ascii);
        // Convert hash to base64url
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashBase64 = hashArray.map(b => String.fromCharCode(b)).join('');
        const hashBase64Url = btoa(hashBase64).replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
        return hashBase64Url;
    }

    let codeVerifier = '';
    let codeChallenge = '';

    onMount(async () => {
        // Generate code verifier and challenge here
        codeVerifier = generateCodeVerifier();
        codeChallenge = await generateCodeChallenge(codeVerifier);

        console.log(codeChallenge);
        console.log(codeVerifier);

        // Save code verifier in local storage
        localStorage.setItem('codeVerifier', codeVerifier);
    });
  
    // Configuration of Authorization endpoint
    const response_type = 'code';
    const client_id = 'aa30af02-f470-4508-880e-8f8c99652143';
    let redirect_uri = 'https://scorpion.bi.denbi.de';
    const scope = 'openid profile email';
    const state = '123456';


    // Function to redirect to the authorization endpoint
    async function authorize() {
        const params = {
            response_type: response_type,
            client_id: client_id,
            redirect_uri: redirect_uri,
            scope: scope,
            state: state,
            code_challenge: codeChallenge,
            code_challenge_method: 'S256'
        }
        const urlParams = new URLSearchParams(params);
        const authUrl = `https://login.aai.lifescience-ri.eu/oidc/authorize?${urlParams.toString()}`;
        window.location.href = authUrl;
    }

  </script>

<div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100 p-4 space-y-2">
    <h1 class="text-2xl font-semibold flex justify-center ">Login</h1>
    <button on:click={authorize}><img src={image} alt="LS Login"/></button>
    <a href="https://signup.aai.lifescience-ri.eu/registrar/?vo=lifescience&group=relying_services%3AScorpion" class="link pr-2 text-xs flex justify-end">Register</a>
</div>