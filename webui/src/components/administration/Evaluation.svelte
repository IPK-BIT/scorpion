<script>
    import { onMount } from "svelte";
    import { loadServices } from "../../lib/api-client/services";
    import { loadMeasurements } from "../../lib/api-client/measurements";
    import { Information } from "carbon-icons-svelte";

    let consortia = [];
    let services = [];

    let licenses = [];

    let selectedConsortium;
    let year = new Date().getFullYear();
    onMount(async () => {
        services = await loadServices();
        consortia = services.filter((s)=> s.category==='Consortia');

        const response = await fetch('https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/json/licenses.json');
        const data = await response.json();
        licenses = data.licenses.filter(license => license.isOsiApproved);
    });

    async function loadConsortiumServiceMeasurements(consortium) {
        let tmp = {};
        let start = new Date(year, 0, 1);
        let stop = new Date(year, 11, 31);
        for (let service of services.filter((s)=>s.consortia.includes(consortium))) {
            let serviceMeasurements = await loadMeasurements(service.abbreviation, start.toISOString(), stop.toISOString());
            let daily = false;
            for (let measurement of serviceMeasurements) {
                if (new Date(measurement.date).toLocaleDateString('en-US').split('/')[1]!="1") {
                    console.log(new Date(measurement.date).getUTCDay(), serviceMeasurements, measurement);
                    daily = true;
                    break;
                }
            }
            if (daily) {
                let measurement = [];
                let yearSum = 0;
                for (let i = 0; i < 12; i++) {
                    let month = new Date(year, i, 1);
                    let sum = 0;
                    for (let m of serviceMeasurements.filter((m)=>new Date(m.date).getMonth()===i && m.kpi===indicators[service.category])) {
                        sum += m.value;
                        yearSum += m.value;
                    }
                    measurement.push({ date: month, value: sum });
                }
                tmp[service.abbreviation] = {'function': "sum", "year": yearSum, 'measurements': measurement};
            } else {
                let measurement = [];
                let yearSum = 0;
                for (let i = 0; i < 12; i++) {
                    let month = new Date(year, i, 1);
                    let tmp = serviceMeasurements.find((m)=>new Date(m.date).getMonth()===i && m.kpi===indicators[service.category]);
                    if (tmp) {
                        measurement.push({ date: month, value: tmp.value });
                    } else {
                        measurement.push({ date: month, value: 0 });
                    }
                    yearSum += tmp?tmp.value:0;
                }
                tmp[service.abbreviation] = {'function': "sum", "year": yearSum, 'measurements': measurement};
            }
        }
        return tmp;
    }

    async function updateConsortiumServiceMeasurements(serviceAbbreviation) {
        let start = new Date(year, 0, 1);
        let stop = new Date(year, 11, 31);
        let result = await loadMeasurements(serviceAbbreviation, start.toISOString(), stop.toISOString());
        let daily = false;
        for (let measurement of result) {
            if (new Date(measurement.date).toLocaleDateString('en-US').split('/')[1]!="1") {
                daily = true;
                break;
            }
        }
        if (daily) {
            let measurement = [];
            let yearValue = 0;
            for (let i=0; i<12; i++) {
                let month = new Date(year, i, 1);
                if (measurements[serviceAbbreviation].function==='sum') {
                    let sum = 0;
                    for (let m of result.filter((m)=>new Date(m.date).getMonth()===i && m.kpi===indicators[services.find((s)=>s.abbreviation===serviceAbbreviation).category])) {
                        sum += m.value;
                        yearValue += m.value;
                    }
                    measurement.push({ date: month, value: sum });
                } else if (measurements[serviceAbbreviation].function==='avg') {
                    let sum = 0;
                    let count = 0;
                    for (let m of result.filter((m)=>new Date(m.date).getMonth()===i && m.kpi===indicators[services.find((s)=>s.abbreviation===serviceAbbreviation).category])) {
                        sum += m.value;
                        count++;
                    }
                    yearValue += sum;
                    measurement.push({ date: month, value: count>0?Math.floor(sum/count):0 });
                } else if (measurements[serviceAbbreviation].function==='min') {
                    let min = Number.MAX_SAFE_INTEGER;
                    for (let m of result.filter((m)=>new Date(m.date).getMonth()===i && m.kpi===indicators[services.find((s)=>s.abbreviation===serviceAbbreviation).category])) {
                        if (m.value<min) {
                            min = m.value;
                            yearValue = m.value;
                        }
                    }
                    if (min===Number.MAX_SAFE_INTEGER) {
                        min = 0;
                    }
                    measurement.push({ date: month, value: min });
                } else if (measurements[serviceAbbreviation].function==='max') {
                    let max = Number.MIN_SAFE_INTEGER;
                    for (let m of result.filter((m)=>new Date(m.date).getMonth()===i && m.kpi===indicators[services.find((s)=>s.abbreviation===serviceAbbreviation).category])) {
                        if (m.value>max) {
                            max = m.value;
                            yearValue = m.value;
                        }
                    }
                    if (max===Number.MIN_SAFE_INTEGER) {
                        max = 0;
                    }
                    measurement.push({ date: month, value: max });
                }
            }
            measurements[serviceAbbreviation] = {'function': measurements[serviceAbbreviation].function, "year": measurements[serviceAbbreviation].function==='avg'?Math.floor(yearValue/12):yearValue, 'measurements': measurement};
        } else {
            let measurement = [];
            let yearValue;
            if (measurements[serviceAbbreviation].function==='sum'||measurements[serviceAbbreviation].function==='avg') {
                yearValue = 0;
            } else if (measurements[serviceAbbreviation].function==='min') {
                yearValue = Number.MAX_SAFE_INTEGER;
            } else if (measurements[serviceAbbreviation].function==='max') {
                yearValue = Number.MIN_SAFE_INTEGER;
            }
            for (let i=0; i<12; i++) {
                let month = new Date(new Date().getFullYear(), i, 1);
                let tmp = result.find((m)=>new Date(m.date).getMonth()===i && m.kpi===indicators[services.find((s)=>s.abbreviation===serviceAbbreviation).category]);
                if (tmp) {
                    measurement.push({ date: month, value: tmp.value });
                    if (measurements[serviceAbbreviation].function==='sum'||measurements[serviceAbbreviation].function==='avg') { 
                        yearValue += tmp.value;
                    } else if (measurements[serviceAbbreviation].function==='min') {
                        if (tmp.value<yearValue) {
                            yearValue = tmp.value;
                        }
                    } else if (measurements[serviceAbbreviation].function==='max') {
                        if (tmp.value>yearValue) {
                            yearValue = tmp.value;
                        }
                    }
                } else {
                    measurement.push({ date: month, value: 0 });
                }
            }
            if (yearValue===Number.MAX_SAFE_INTEGER) {
                yearValue = 0;
            } else if (yearValue===Number.MIN_SAFE_INTEGER) {
                yearValue = 0;
            }
            measurements[serviceAbbreviation] = {'function': measurements[serviceAbbreviation].function, "year": measurements[serviceAbbreviation].function==='avg'?Math.floor(yearValue/12):yearValue, 'measurements': measurement};
        }
    }

    let measurements = {};
    $: console.log(measurements);


    let indicators = {
        'Databases': 'Visits',
        'Webapplications': 'Visits',
        'Tools': 'Downloads',
        'Libraries': 'Downloads',
        'Workflows': 'Executions',
        'Supports': 'Support Tickets',
        'Trainings': 'Events',
    }

    
    // $: console.log(licenses);
    // $: console.log(services);
</script>

<label class="select w-full">
    <span class="label">Consortium</span>
    <select bind:value={selectedConsortium} on:change={async () => measurements = await loadConsortiumServiceMeasurements(selectedConsortium)}>
        <option disabled selected value={undefined}>Select a consortium</option>
        {#each consortia.sort((a,b)=>a.name.localeCompare(b.name)) as consortium}
            <option disabled={services.filter((s)=>s.consortia.includes(consortium.name)).length==0}>{consortium.name}</option>
        {/each}
    </select>
</label>

{#if selectedConsortium}
<section class="py-4">
    <div class="stats shadow bg-white w-full">
        <div class="stat space-y-2">
            <div class="stat-title font-semibold">Total Services Provided</div>
            <div class="stat-value text-accent text-center text-5xl">{services.filter((service) => service.consortia.includes(selectedConsortium)).length}</div>
        </div>
        <div class="stat space-y-2">
            <div class="stat-title font-semibold">
                <div class="flex flex-row items-center space-x-1">
                    <p>
                        Open Source Services
                    </p>
                    <div class="tooltip tooltip-bottom tooltip-info" data-tip="Follows OSI Approvals">
                    <span class="h-2 w-2"><Information/></span>
                    </div>
                </div>                
            </div>
            <div class="stat-value text-accent text-center text-5xl">{services.filter((s)=>s.category!='Consortia' && s.consortia.includes(selectedConsortium) && licenses.map(l=>l.licenseId).includes(s.license)).length}</div>
        </div>
        <div class="stat space-y-2">
            <div class="stat-title font-semibold">Services in Development Stage</div>
            <div class="stat-value text-accent text-center text-5xl">{services.filter((s)=>s.consortia.includes(selectedConsortium) && s.stage==='dev').length}</div>
        </div>
        <div class="stat space-y-2">
            <div class="stat-title font-semibold">Services in Prototype Stage</div>
            <div class="stat-value text-accent text-center text-5xl">{services.filter((s)=>s.consortia.includes(selectedConsortium) && s.stage==='demo').length}</div>
        </div>
        <div class="stat space-y-2">
            <div class="stat-title font-semibold">Services in Production Stage</div>
            <div class="stat-value text-accent text-center text-5xl">{services.filter((s)=>s.consortia.includes(selectedConsortium) && s.stage==='prod').length}</div>
        </div>
    </div>
    <div class="shadow rounded-box bg-white w-full mt-4 p-4">
        <table class="table">
            <thead>
                <tr>
                    <th>Service</th>
                    <th class="border-r border-neutral-300">Function</th>
                    {#each Array.from({ length: 12 }, (_, i) => i + 1) as month}
                    <th class="text-center">{new Date(0, month - 1).toLocaleString('en-US', { month: 'short' })}</th>
                    {/each}
                    <th class="border-l border-neutral-300">
                        <input class="input input-sm" type="number" min={1970} max={2100} bind:value={year} on:change={async ()=>{measurements = await loadConsortiumServiceMeasurements(selectedConsortium)}}/>
                    </th>
                </tr>
            </thead>
            <tbody>
                {#each services.filter((service) => service.consortia.includes(selectedConsortium)).sort((a,b)=>a.name.localeCompare(b.name)) as service}
                {#if measurements[service.abbreviation] && measurements[service.abbreviation].measurements}
                <tr class="hover:bg-accent">
                    <th>
                        <p>{service.name}</p>
                        <p class="text-xs italic font-normal">({indicators[service.category]})</p>
                    </th>
                    <td class="border-r border-neutral-300">
                        <select class="select select-sm" bind:value={measurements[service.abbreviation].function} on:change={()=>updateConsortiumServiceMeasurements(service.abbreviation)}>
                            <option value="sum">sum</option>
                            <option value="avg">avg</option>
                            <option value="min">min</option>
                            <option value="max">max</option>
                        </select>
                    </td>
                    {#each measurements[service.abbreviation].measurements as measurement}
                    <td class="text-center">{measurement.value}</td>
                    {/each}
                    <th class="border-l border-neutral-300 text-center">{measurements[service.abbreviation].year}</th>
                </tr>
                {/if}
                {/each}
            </tbody>
        </table>
    </div>
</section>
{/if}