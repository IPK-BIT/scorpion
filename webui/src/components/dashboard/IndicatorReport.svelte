<script>
    export let indicator = {};

    function extract(kpi) {
        let values = Object.values(kpi).filter((v)=>typeof v === 'number');
        return {
            min: Math.min(...values),
            max: Math.max(...values),
            avg: values.reduce((a,b)=>a+b, 0)/values.length,
        }
    }

    let stats;
    $: stats = extract(indicator);
</script>

<div class="stat">
    <div class="stat-title">{indicator.name}</div>
    <div class="stat-value text-primary">{(Math.floor(stats.avg*100)/100).toLocaleString()}</div>
    <div class="stat-desc">Min: {stats.min.toLocaleString()} - Max: {stats.max.toLocaleString()}</div>
</div>