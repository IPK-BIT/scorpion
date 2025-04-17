<script>
    import axios from "axios";
    import { api } from "../stores/api";
    import { onMount } from "svelte";
    import Card from "../components/Card.svelte";
    import { AddAlt, Close, Copy, TrashCan } from "carbon-icons-svelte";

    let user = {};
    let providers = [];

    let selected_provider = '';
    let tokenName = '';
    let newToken = '';
    let openRequests = [];

    async function requestMembership() {
		const response = await axios.post(
			'/requests/membership',
			{},
			{
				baseURL: $api.base_url + $api.modules.aai,
				params: { providers: selected_provider }
			}
		);
		if (response.status === 201) {
			openRequests = [
				...openRequests,
				...[{ id: '', mail: '', username: '', provider: selected_provider }]
			];
			selected_provider = '';
		}
	}

    async function createNewToken() {
		const response = await axios.post(
			'/tokens',
			{
				name: tokenName
			},
			{
				baseURL: $api.base_url + $api.modules.aai
			}
		);
		if (response.status === 200) {
			newToken = response.data;
			user.tokens = [tokenName, ...user.tokens];
		}
	}

	async function deleteToken(token) {
        newToken = '';
		const response = await axios.delete('/tokens', {
			baseURL: $api.base_url + $api.modules.aai,
			params: { token: token }
		});
		if (response.data) {
			user.tokens = user.tokens.filter((t) => t !== token);
		}
	}

    function copyToClipboard() {
        navigator.clipboard.writeText(newToken);
        alert('Token copied to clipboard');
    }

    onMount(async () => {
        let response = await axios.get(`${$api.base_url}${$api.modules.aai}/details`);
        user = response.data;
        response = await axios.get(`${$api.base_url}${$api.modules.aai}/tokens`);
        user.tokens = response.data;

        response = await axios.get('/requests/membership', {
			baseURL: $api.base_url + $api.modules.aai
		});
        openRequests = response.data;

        response = await axios.get(`${$api.base_url}${$api.modules.v1}/providers`);
        providers = response.data.result;

        console.log(user, providers)
    });
</script>

<div class="w-1/2 m-auto">
    <Card title="User Profile">
        <div slot="card-content">
            <fieldset class="fieldset bg-base-200 border border-base-300 p-4 rounded-box">
                <legend class="fieldset-legend">User Details</legend>

                <label for="username" class="fieldset-label">Username</label>
                <input type="text" id="username" class="input w-full" value={user.user_name} readonly />

                <label for="email" class="fieldset-label">Email</label>
                <input type="text" id="email" class="input w-full" value={user.email} readonly />
            </fieldset>

            <fieldset class="fieldset bg-base-200 border border-base-300 p-4 rounded-box">
                <legend class="fieldset-legend">Provider Memberships<label for="provider-modal" class="text-primary btn btn-circle btn-ghost btn-xs"><AddAlt/></label></legend>

                <ul class="list bg-base-100 border border-base-300 rounded-box">
                    {#each user.providers as provider}
                    <li class="list-row">
                        <p>{provider}</p>
                    </li>
                    {/each}
                    {#each openRequests as request}
                    <li class="list-row">
                        <p class="opacity-50">{request.provider}</p>
                    </li>
                    {/each}
                </ul>
            </fieldset>

            {#if newToken}
            <fieldset class="fieldset bg-white border-2 border-warning border-dashed p-4 rounded-box mt-4">
                <!-- <legend class="fieldset-legend">New Token</legend> -->
                <div class="join w-full input border border-dashed border-neutral rounded-md bg-white">
                    <input value={newToken} readonly class="join-item"/>
                    <button class="join-item" on:click={copyToClipboard}><Copy/></button>
                </div>
                
                <p class="fieldset-label">Copy the Token and store it securely, you will not be able to read this token again.</p>
            </fieldset>
            {/if}

            <fieldset class="fieldset bg-base-200 border border-base-300 p-4 rounded-box">
                <legend class="fieldset-legend">Tokens<label for="token-modal" class="text-primary btn btn-circle btn-ghost btn-xs"><AddAlt/></label></legend>

                <ul class="list bg-base-100 border border-base-300 rounded-box">
                    {#each user.tokens as token}
                    <li class="list-row flex justify-between items-center">
                        <p>{token}</p>
                        <button class="btn btn-circle btn-secondary hover:btn-error" on:click={()=>{deleteToken(token)}}><TrashCan/></button>
                    </li>
                    {/each}
                </ul>
        </div>
    </Card>

</div>


<input type="checkbox" id="provider-modal" class="modal-toggle" />
<div class="modal">
	<form method="dialog" class="modal-box">
		<label for="provider-modal" class="btn btn-circle btn-ghost absolute right-2 top-2"><Close size={32} /></label>
		<h3 class="font-bold text-lg">Request Membership</h3>
		<div class="my-2">
			<label class="select w-full">
                <span class="label">Service Provider</span>
                <select bind:value={selected_provider}>
                    <option disabled selected value="">Select an option</option>
                    {#each providers as provider}
                    {#if !user.providers.includes(provider.abbreviation)}
                        <option value={provider.abbreviation}>{provider.name}</option>
                    {/if}
                    {/each}
                </select>
            </label>
		</div>
		<div class="flex justify-end">
			<!-- svelte-ignore a11y_click_events_have_key_events -->
			<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
			<label for="provider-modal" class="btn btn-primary" on:click={requestMembership}>Request Membership</label>
		</div>
	</form>
</div>

<input type="checkbox" id="token-modal" class="modal-toggle" />
<div class="modal">
	<form method="dialog" class="modal-box">
		<label for="token-modal" class="btn btn-circle btn-ghost absolute right-2 top-2"><Close size={32} /></label>
		<h3 class="font-bold text-lg">Request API Token</h3>
		<div class="my-2">
            <label class="input w-full">
                <span class="label">Token Name</span>
                <input type="text" bind:value={tokenName}/>
            </label>
		</div>
		<div class="flex justify-end">
			<!-- svelte-ignore a11y_click_events_have_key_events -->
			<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
			<label for="token-modal" class="btn btn-primary" on:click={createNewToken}>Request API Token</label>
		</div>
	</form>
</div>