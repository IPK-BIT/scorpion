<script>
    import indicator from "daisyui/components/indicator";
    import IndicatorReport from "./IndicatorReport.svelte";
    import { Download } from "carbon-icons-svelte";

    export let result_table = [];
    export let daily = false;

    function transform(table) {
        let transformed_table = [];
        for (let row of table) {
            for (let key of Object.keys(row)) {
                if (key!='date') {
                    let transformed_row = transformed_table.find((r)=>r.name === key);
                    if (transformed_row) {
                        transformed_row[row['date']] = row[key];
                    } else {
                        let new_row = {
                            name: key,
                        }
                        new_row[row['date']] = row[key];
                        transformed_table.push(new_row);
                    }
                }
            }
        }
        console.log(transformed_table);
        return transformed_table;
    }
    let data;
    let dates;

    $: dates = new Set(result_table.map((r)=>r.date));
    $: data = transform(result_table);

    function download() {
        let csv = 'data:text/csv;charset=utf-8,';
        csv += 'Indicator;'+Array.from(dates).map((d)=>new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric'})).join(';')+'\n';
        for (let indicator of data) {
            csv += indicator.name+';'+Array.from(dates).map((d)=>indicator[d]||'').join(';')+'\n';
        }
        let encodedUri = encodeURI(csv);
        let link = document.createElement('a');
        link.setAttribute('href', encodedUri);
        link.setAttribute('download', 'kpi-report.csv');
        document.body.appendChild(link);
        link.click();
    }

</script>

<section class="space-y-2">
    <div class="flex flex-row justify-end">
        <button class="btn btn-primary" on:click={download}>Export<Download /></button>
    </div>
    <div class="overflow-auto">
        <table class="table">
            <thead>
                <tr>
                    <th>Indicator</th>
                    {#each dates as date}
                    {#if daily}
                    <th>{new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric'})}</th>
                    {:else}
                    <th>{new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'short' })}</th>
                    {/if}
                    {/each}
                </tr>
            </thead>
            <tbody>
                {#each data.sort((a,b)=>a.name.localeCompare(b.name)) as indicator}
                <tr class="hover:bg-secondary">
                    <td>{indicator.name}</td>
                    {#each dates as date}
                    <td>{indicator[date]}</td>
                    {/each}
                </tr>
                {/each}
            </tbody>
        </table>
    </div>
    <div class="stats shadow bg-base-100 w-full">
    {#each data.sort((a,b)=>a.name.localeCompare(b.name)) as indicator}
    <IndicatorReport bind:indicator />
    {/each}
    </div>
</section>