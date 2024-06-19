<script lang="ts">
	import { UserAvatarFilled } from 'carbon-icons-svelte';
	import Card from '../pageContents/Card.svelte';
	import axios from 'axios';
	import { api } from '$lib/stores/api';
	import { registration_requests, users } from '$lib/stores/admin';

	async function answerRequest(request_id: string, decision: boolean) {
		const response = await axios.delete('/requests/registration', {
			baseURL: $api.base_url + $api.modules.aai,
			params: {
				request_id: request_id,
				is_admin: $registration_requests.find((r) => {
					return r.user_id === request_id;
				})?.is_admin,
				accept: decision
			}
		});
		if (response.status === 200) {
			if (decision) {
				let request = $registration_requests.find((r) => {
					return r.user_id === request_id;
				});
				if (request === undefined) {
					request = {
						user_id: '',
						user_name: '',
						email: '',
						is_admin: false
					};
				}
				$users = [
					...$users,
					{
						user_name: request.user_name,
						email: request.email,
						providers: [],
						is_admin: request.is_admin != null ? request.is_admin : false
					}
				];
			}
			$registration_requests = $registration_requests.filter((r) => {
				return r.user_id != request_id;
			});
		}
	}
</script>

<Card title="Registration Requests">
	<div slot="card-content">
		<div class="overflow-x-auto">
			<table class="table">
				<!-- head -->
				<thead>
					<tr>
						<th>User</th>
						<th>Administrator</th>
						<th />
					</tr>
				</thead>
				<tbody>
					{#if $registration_requests.length === 0}
						<tr> There are currently no open requests </tr>
					{/if}
					{#each $registration_requests as request}
						<tr>
							<td>
								<div class="flex items-center space-x-3">
									<div class="avatar">
										<div class="mask mask-squircle w-12 h-12">
											<svg class="w-12 h-12" viewBox="0 0 24 24">
												<UserAvatarFilled size={24} />
											</svg>
										</div>
									</div>
									<div>
										<div class="font-bold">{request.user_name}</div>
										<div class="text-sm opacity-50">{request.email}</div>
									</div>
								</div>
							</td>
							<td>
								<input type="checkbox" class="checkbox" bind:checked={request.is_admin} />
							</td>
							<th class="text-center">
								<button
									class="btn btn-ghost hover:btn-success"
									on:click={() => {
										answerRequest(request.user_id, true);
									}}>Accept</button
								>
								<button
									class="btn btn-ghost hover:btn-error"
									on:click={() => {
										answerRequest(request.user_id, false);
									}}>Decline</button
								>
							</th>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</Card>
