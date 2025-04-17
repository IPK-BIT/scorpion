<script>
    import { onMount } from 'svelte';
    import PolicyDisplay from '../components/footer/PolicyDisplay.svelte';
    import Card from '../components/Card.svelte';
    import { MailAll } from 'carbon-icons-svelte';
    import { config } from '../lib/scorpion.config';

    let hash;

    onMount(() => {
        hash = window.location.hash;
    });
</script>

{#if hash==='#/terms-of-use'}
<PolicyDisplay link='/terms-of-use.html' title='Terms of Use'/>
{:else if hash==='#/privacy'}
<PolicyDisplay link='/privacy-policy.html' title='Privacy Policy'/>
{:else if hash==='#/contact'}
<div class="w-1/2 m-auto">
    <Card title="Contact Us">
        <div slot="card-content">
            <ul class="list bg-base-200 border border-base-300 rounded-box shadow-md">           
                {#each config.contacts as contact}
                <li class="list-row flex justify-between items-center">
                  <div>
                    <div>{contact.name}</div>
                    <div class="text-xs uppercase font-semibold opacity-60">{contact.role}</div>
                  </div>
                  <a href="mailto:{contact.email}"><MailAll size={24}/></a>
                </li>                
                {/each}    
              </ul>
        </div>
    </Card>       
</div>
{:else if hash==='#/how-to-cite'}
<div class="w-1/2 m-auto">
    <Card title="How to Cite">
        <div slot="card-content">
            <div>
                <p>When using Scorpion, please cite the following publication:</p>
                <p class="bg-base-200 p-2 rounded-md mt-2 ml-2">{config.citation.service}</p>
            </div>
            <div>
                <p>Additionally, please cite the following publication for the underlying software:</p>
                <p class="bg-base-200 p-2 rounded-md mt-2 ml-2">{config.citation.software}</p>
            </div>            
        </div>
    </Card>

</div>
{:else if hash==='#/about'}
<PolicyDisplay link='/about.html' title='About'/>
{/if}