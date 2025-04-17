<script>
    import Card from "./Card.svelte";

    let news = [
        {
            headline: "Headline",
            subheader: "Subheader",
            content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac purus sit amet nunc fermentum aliquam. Nullam fringilla, nunc in ultricies ultricies, nunc ipsum ultricies nunc, nec malesuada nunc metus a nunc. Nullam fringilla, nunc in ultricies ultricies, nunc ipsum ultricies nunc, nec malesuada nunc metus a nunc."
        }
    ]
</script>
<!-- <Card title="News"> -->
<ul class="list ">
    {#if news.length === 0}
    <li class="list-row">
        <div class="text-center">No news available</div>
    </li>
    {/if}
    {#each news as n}
    <li class="list-row">
        <div>
            <div>{n.headline}</div>
            <div class="text-xs uppercase font-semibold opacity-60">{n.subheader}</div>
        </div>
        <p class="list-col-wrap text-xs">
            {n.content}
        </p>
    </li>
    {/each}
</ul>
<!-- </Card> -->