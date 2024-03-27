<svelte:head>
<title>About</title>
<meta name="description" content="Service Monitoring KPI Dashboard of NFDI4Biodiversity Description" />
<script src="https://cdn.plot.ly/plotly-latest.min.js" type="text/javascript"></script>	
</svelte:head>

<div class="flex flex-col p-8 space-y-4">
	<h1 class="flex justify-center text-4xl font-bold">About Scorpion</h1>
	<section class="pt-4 flex justify-center">
		<p class="text-lg w-[50%]">
			Scorpion is designed as a central platform to collect and store the KPI set and its category assignments, the service KPI sets and the service KPI measurements. It is hosted at the de.NBI cloud and maintained by the IPK and implements a basic role-based access (RBAC) model, distinguishing between users and administrators. 
			Administrators can manage the users, KPI measurements and generate report cards. Users can either visualise the KPI measurements per service or submit results to the dashboard via the graphical user interface (GUI) or a RESTful API.
			For transparency, the results can be viewed by any user for any service.
		</p>
	</section>	
	<h2 class="flex justify-center text-3xl font-semibold">Service Registration</h2>
	<section class="pt-4 flex justify-center">
		<div class="text-lg w-[50%]">
			<p>
				In the current version of Scorpion, the services are registered through a form in this web application. The form is available at the <a class="link" href="/bonsai">Service Registration</a> page. The form requires the following information:
			</p>
			<ul class="space-y-2 bg-white rounded-lg shadow-md p-4 m-4">
				<li>Service Short Name</li>
				<li>Service Provider</li>
				<li>Service Category</li>
				<li>(optional) additional KPIs</li>
			</ul>
			<p>
				In future versions, a stand-alone tool will be provided to register services. The tool will be available as a docker container and will be accessible via a RESTful API.
			</p>
		</div>
	</section>
</div>		