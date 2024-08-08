<svelte:head>
	<title>About</title>
	<meta
		name="description"
		content="Service Monitoring KPI Dashboard of NFDI4Biodiversity Description"
	/>
	<script src="https://cdn.plot.ly/plotly-latest.min.js" type="text/javascript"></script>
</svelte:head>

<div class="flex flex-col p-8 space-y-4">
	<h1 class="flex justify-center text-4xl font-bold">About Scorpion</h1>
	<section class="pt-4 flex justify-center">
		<p class="text-lg w-[50%]">
			Scorpion is designed as a central platform to collect and store the KPI set and its category
			assignments, the service KPI sets and the service KPI measurements. It is hosted at the de.NBI
			cloud and maintained by the IPK and implements a basic role-based access (RBAC) model,
			distinguishing between users and administrators. Administrators can manage the users, KPI
			measurements and generate report cards. Users can either visualise the KPI measurements per
			service or submit results to the dashboard via the graphical user interface (GUI) or a RESTful
			API. For transparency, the results can be viewed by any user for any service.
		</p>
	</section>
	<h2 class="flex justify-center text-3xl font-semibold">Service Registration</h2>
	<section class="pt-4 flex justify-center">
		<div class="text-lg w-[50%]">
			<p>
				In the current version of Scorpion, the services are registered through a form in this web
				application. The form is available at the <a class="link" href="/register"
					>Service Registration</a
				> page. The form queries the following information:
			</p>
			<ul class="space-y-2 bg-white rounded-lg shadow-md p-4 m-4">
				<li>Service Abbreviation</li>
				<li>Service Name</li>
				<li>Service Provider</li>
				<li>(optional) License</li>
				<li>(optional) Development Stage</li>
				<li>Service Category</li>
				<li>(optional) additional KPIs</li>
			</ul>
		</div>
	</section>
	<h2 class="flex justify-center text-3xl font-semibold">Personal Data</h2>
	<section class="pt-4 flex justify-center">
		<div class="text-lg w-[50%]">
			<p>
				Scorpion stores personal data of its user as provided through the AAI. This data is used to
				identify users when requesting membership to Service Providers. The stored information can
				be viewed in the <a href="/users/me" class="link">user profile</a>. The personal data
				includes the scopes as agreed in the login process:
			</p>
			<ul class="space-y-2 bg-white rounded-lg shadow-md p-4 m-4">
				<li>LS Identifier</li>
				<li>Email</li>
				<li>Profile</li>
			</ul>
		</div>
	</section>
</div>
