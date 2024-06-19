<script lang="ts">
	import { goto } from '$app/navigation';
	import { token } from '$lib/stores/api';
	import image from '$lib/assets/favicon.png';
	import { Locked, Menu, UserFilled } from 'carbon-icons-svelte';
</script>

<div class="navbar bg-neutral">
	<div class="dropdown">
		<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
		<!-- svelte-ignore a11y-label-has-associated-control -->
		<label tabindex="0" class="btn btn-ghost btn-circle text-white">
			<Menu />
		</label>
		<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
		<ul
			id="navbarmenu"
			tabindex="0"
			class="dropdown-content menu p-2 shadow bg-base-200 rounded-box w-52 z-10"
		>
			<li><a href="/register">Service Registration</a></li>
			<li><a href="/submit">KPI Submission</a></li>
			<li><a class="hover:bg-warning" href="/administration">Administration<Locked /></a></li>
		</ul>
	</div>
	<div class="flex-1">
		<a href="/" class="btn btn-ghost normal-case text-xl text-white">Scorpion</a>
		<img src={image} style="height: 2em;" alt="Scorpion Icon" />
	</div>
	<div class="flex-none">
		<div class="dropdown dropdown-end">
			<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
			<!-- svelte-ignore a11y-label-has-associated-control -->
			<label tabindex="0" class="btn btn-ghost btn-circle text-white">
				<div class="indicator">
					<UserFilled size={24} />
				</div>
			</label>
			<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
			<ul
				tabindex="0"
				class="menu menu-compact dropdown-content mt-3 p-2 shadow bg-base-200 rounded-box w-52 z-10"
			>
				<li><a href="/users/me">Profile</a></li>
				<li><a href="/about">About</a></li>
				<li><a href="/docs">API Docs</a></li>
				<!-- svelte-ignore a11y-missing-attribute -->
				<li>
					<button
						class="hover:bg-error"
						on:click={() => {
							token.set('');
							localStorage.setItem('token', '');
							goto('/');
						}}>Logout</button
					>
				</li>
			</ul>
		</div>
	</div>
</div>
