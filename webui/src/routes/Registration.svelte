<script>
    import RegistrationForm from "../components/registration/RegistrationForm.svelte";
    import { config } from "../lib/scorpion.config";

    let activatedProfiles = config.default_profiles;

    function toggleProfile(profile) {
        if (activatedProfiles.includes(profile)) {
            activatedProfiles = activatedProfiles.filter((item) => item !== profile);
        } else {
            activatedProfiles = [...activatedProfiles, profile];
        }
    }

</script>

<section class="flex flex-row mb-2">
    <div class="w-1/5 mx-2">
        <ul class="list bg-base-200 rounded-box shadow-md border border-base-300 w-5/6">
            <li class="p-4 pb-2 text-xs opacity-60 tracking-wide">Metadata Profiles</li>
            {#each config.service_profiles as profile}
            <li class="list-row flex justify-between">
                <div>
                    <div class="font-semibold">{profile.name}</div>
                    <div class="text-xs opacity-60">{profile.description}</div>
                </div>
                <input type="checkbox" class="checkbox" checked={activatedProfiles.includes(profile.id)} on:change={()=>toggleProfile(profile.id)}/>
            </li>
           {/each}
        </ul>
    </div>
    <div class="w-3/5">
        <RegistrationForm profile_ids={activatedProfiles}/>
    </div>
</section>