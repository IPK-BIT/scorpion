<script lang="ts">
	import type { MembershipRequest, ServiceProvider, UserDetail } from '$lib/stores/types';
	import { Add, Close } from 'carbon-icons-svelte';
	import Card from '../pageContents/Card.svelte';
	import { api } from '$lib/stores/api';
	import axios from 'axios';

	let selected_provider: string = '';
	let tokenName: string = '';
	let tokenValue: string = '';

	export let tokens: string[] = [];

	async function createNewToken() {
		console.log(tokenName);
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
			tokenValue = response.data;
			tokens = [tokenName, ...tokens];
		}
	}

	async function deleteToken(token: string) {
		const response = await axios.delete('/tokens', {
			baseURL: $api.base_url + $api.modules.aai,
			params: { token: token }
		});
		if (response.data) {
			tokens = tokens.filter((t) => t !== token);
		}
	}

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

	function openTokenModal() {
		document.getElementById('my_modal_4')?.showModal();
	}

	export let providers: ServiceProvider[];
	export let details: UserDetail;
	export let openRequests: MembershipRequest[];
</script>

<div class="flex flex-col p-4 space-y-4">
	<Card title="User Information">
		<div slot="card-content" class="form-control space-y-4">
			<div class="space-y-2">
				<label class="input-group">
					<span class="w-1/12 label-text">Username</span>
					<input
						type="text"
						disabled
						class="w-11/12 input input-bordered"
						bind:value={details.user_name}
					/>
				</label>
				<label class="input-group">
					<span class="w-1/12 label-text">Email</span>
					<input
						type="text"
						disabled
						class="w-11/12 input input-bordered"
						bind:value={details.email}
					/>
				</label>
			</div>
			<div class="divider">Roles</div>
			<label class="label cursor-pointer">
				<span class="label-text">Admin</span>
				<input type="checkbox" disabled bind:checked={details.is_admin} class="checkbox" />
			</label>
			<div class="divider">
				Service Provider Memberships
				<button class="btn btn-circle btn-accent btn-sm" onclick="my_modal_3.showModal()"
					><Add /></button
				>
			</div>
			{#each details.providers as provider}
				<label class="label cursor-pointer">
					<span class="label-text">{provider}</span>
					<input type="checkbox" disabled checked class="checkbox" />
				</label>
			{/each}
			{#each openRequests as request}
				<label class="label cursor-pointer">
					<span class="label-text text-gray-200">{request.provider}</span>
					<input type="checkbox" disabled class="checkbox" />
				</label>
			{/each}
			<div class="divider">API Keys</div>
			<div class="flex justify-end">
				<button class="btn btn-info btn-sm" on:click={openTokenModal}>Create API Key</button>
			</div>
			<table class="table">
				<!-- <thead>
					<th>API Key</th>
					<th>Action</th>
				</thead> -->
				<tbody class="table-zebra">
					{#each tokens as token}
						<tr>
							<td>{token}</td>
							<td
								><button
									class="btn btn-sm hover:btn-error"
									on:click={() => {
										deleteToken(token);
									}}>DELETE</button
								></td
							>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</Card>
</div>

<dialog id="my_modal_3" class="modal">
	<form method="dialog" class="modal-box">
		<button class="btn btn-circle btn-ghost absolute right-2 top-2"><Close size={32} /></button>
		<h3 class="font-bold text-lg">Request Membership</h3>
		<div class="join w-full py-2">
			<label for="provider" class="join-item bg-base-300 label label-text w-[30%]"
				>Service Provider</label
			>
			<select
				id="provider"
				class="join-item select select-bordered w-[70%]"
				bind:value={selected_provider}
			>
				<option disabled selected value="">Select a Service Provider</option>
				{#each providers as provider}
					<option value={provider.abbreviation}>{provider.name}</option>
				{/each}
			</select>
		</div>
		<div class="flex justify-end">
			<button class="btn btn-secondary" on:click={requestMembership}>Request Membership</button>
		</div>
	</form>
</dialog>

<dialog id="my_modal_4" class="modal">
	<div class="modal-box">
		<form method="dialog">
			<button class="btn btn-circle btn-ghost absolute right-2 top-2"><Close size={32} /></button>
		</form>
		{#if !tokenValue}
			<h3 class="font-bold text-lg">Create API Key</h3>
			<div class="join w-full py-2">
				<label class="label space-x-2">
					<span class="label-text">Name</span>
					<input class="input input-bordered input-sm" bind:value={tokenName} />
				</label>
			</div>
			<div class="flex justify-end">
				<button class="btn btn-secondary" on:click={createNewToken}>Create API Key</button>
			</div>
		{:else}
			<h3 class="font-bold text-lg">API Key</h3>
			<div class="bg-warning p-2 rounded-md">
				Make sure you safe the API Key securely, you won't be able to see it again!
			</div>
			<div class="join w-full py-2">
				<div class="p-2 bg-neutral-50 border border-dashed flex justify-center w-full">
					<span>{tokenValue}</span>
				</div>
			</div>
			<div class="flex justify-end">
				<button
					class="btn btn-secondary"
					on:click={() => {
						tokenValue = '';
						document.getElementById('my_modal_4')?.close();
					}}>Close</button
				>
			</div>
		{/if}
	</div>
</dialog>
