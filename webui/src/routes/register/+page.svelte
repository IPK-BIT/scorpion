<script lang="ts">
    import axios from "axios";
    import UploadCard from "$lib/components/bonsai/UploadCard.svelte";
    import GeneralInformationForm from "$lib/components/bonsai/forms/GeneralInformationForm.svelte";
    import type { Metadata } from "$lib/stores/types";
    import OrganizationalInformationForm from "$lib/components/bonsai/forms/OrganizationalInformationForm.svelte";
    import SupportForm from "$lib/components/bonsai/forms/SupportForm.svelte";
    import TechnicalInfrastructureForm from "$lib/components/bonsai/forms/TechnicalInfrastructureForm.svelte";
    import DocumentationForm from "$lib/components/bonsai/forms/DocumentationForm.svelte";
    import ReportingForm from "$lib/components/bonsai/forms/ReportingForm.svelte";
    import { api } from "$lib/stores/api";
    import { Close, Warning } from "carbon-icons-svelte";
    
    let metadata:Metadata = {
        name: "",
        abbreviation: "",
        provider: "",
        areaofapplication: {
            planning: false,
            harmonization: false,
            access: false,
            discover: false,
            processing: false,
            support: false
        },
        description: "",
        inputformats: "",
        outputformats: "",
        developmentstage: "",
        version: "",
        documentation: "",
        license: "",
        link: "",
        serviceorientation: "",
        includeincataglog: "",
        serviceprovidedas: {
            institutionalMission: {
                partOf: false,
                percentage: 0
            },projectFunding: {
                partOf: false,
                percentage: 0
            },others: {
                partOf: false,
                percentage: 0
            }
        },
        funding: "",
        contact: "",
        helpdesk: "",
        supporteduntil: "",
        technicalbackbone: "",
        disasterplan: "",
        entrancecontrol: "",
        operationstability: "",
        templates: "",
        communication: "",
        registered: {
            biotools: {
                registered: false,
                url: ""
            },risources: {
                registered: false,
                url: ""
            },eosc: {
                registered: false,
                url: ""
            },fairsharing: {
                registered: false,
                url: ""
            },re3data: {
                registered: false,
                url: ""
            },others: {
                registered: false,
                url: ""
            },
        },
        publications: "",
        category: "",
        additionalKPI: []
    };
    
    let currentStep: 0|1|2|3|4|5 = 0;
    let steps: {
        active: "step-primary"|"", 
        title: string
    }[] = [{
        active: "step-primary", 
        title: "General Information"
    }, 
    // {
    //     active: "", 
    //     title: "Organizational Information"
    // },{
    //     active: "", 
    //     title: "Support"
    // }, {
    //     active: "", 
    //     title: "Technical Infrastructure"
    // }, {
    //     active: "", 
    //     title: "Documentation"
    // }, 
    {
        active: "", 
        title: "Reporting"
    }]   
    
    function navigate(direction: 'previous'|'next') {
        if(validatePage()) {
            direction==='previous'?currentStep--:currentStep++;
            direction==='previous'?steps[currentStep+1].active="":steps[currentStep].active="step-primary";
        }
    }        
    
    function validatePage() {
        validationErrors=validationErrors.filter((e)=>{return e.type==="warning"});
        let valid = true;
        if(currentStep===0) {
            if(metadata.name.length===0) {
                validationErrors=[...validationErrors, {type: "error", message: "Name is missing"}]
                valid=false;
            }
            if(metadata.abbreviation.length===0) {
                validationErrors=[...validationErrors, {type: "error", message: "Abbreviation is missing"}]
                valid=false;
            }
            if(metadata.abbreviation.length>20) {
                validationErrors=[...validationErrors, {type: "error", message: "Abbreviation is too long"}]
                valid=false;
            }
            if(metadata.provider==="") {
                validationErrors=[...validationErrors, {type: "error", message: "Provider is missing"}]
                valid=false;
            }
            // if(metadata.description.length===0) {
            //     validationErrors=[...validationErrors, {type: "error", message: "Description is missing"}]
            //     valid=false;
            // }
        // } else if (currentStep===2) {
        //     if (metadata.contact.length===0) {
        //         validationErrors=[...validationErrors, {type: "error", message: "Contact is missing"}]
        //         valid=false;
        //     }
        // } else if (currentStep===4) {
        //     if (metadata.registered.biotools.url.length>0 && !isValidHttpUrl(metadata.registered.biotools.url)) {
        //         if (!validationErrors.find((e)=>{return e.message==="Biotools: Invalid URL"})) {
        //             validationErrors=[...validationErrors, {type: "warning", message: "Biotools: Invalid URL"}]
        //         }
        //     } else {
        //         validationErrors=validationErrors.filter((e)=>{return e.message!="Biotools: Invalid URL"})
        //     }
        //     if (metadata.registered.risources.url.length>0 && !isValidHttpUrl(metadata.registered.risources.url)) {
        //         if (!validationErrors.find((e)=>{return e.message==="DFG RIsources: Invalid URL"})) {
        //             validationErrors=[...validationErrors, {type: "warning", message: "DFG RIsources: Invalid URL"}]
        //         }
        //     } else {
        //         validationErrors=validationErrors.filter((e)=>{return e.message!="DFG RIsources: Invalid URL"})
        //     }
        //     if (metadata.registered.eosc.url.length>0 && !isValidHttpUrl(metadata.registered.eosc.url)) {
        //         if (!validationErrors.find((e)=>{return e.message==="EOSC Marketplace: Invalid URL"})) {
        //             validationErrors=[...validationErrors, {type: "warning", message: "EOSC Marketplace: Invalid URL"}]
        //         }
        //     } else {
        //         validationErrors=validationErrors.filter((e)=>{return e.message!="EOSC Marketplace: Invalid URL"})
        //     }
        //     if (metadata.registered.fairsharing.url.length>0 && !isValidHttpUrl(metadata.registered.fairsharing.url)) {
        //         if (!validationErrors.find((e)=>{return e.message==="FAIRsharing: Invalid URL"})) {
        //             validationErrors=[...validationErrors, {type: "warning", message: "FAIRsharing: Invalid URL"}]
        //         }
        //     } else {
        //         validationErrors=validationErrors.filter((e)=>{return e.message!="FAIRsharing: Invalid URL"})
        //     }
        //     if (metadata.registered.re3data.url.length>0 && !isValidHttpUrl(metadata.registered.re3data.url)) {
        //         if (!validationErrors.find((e)=>{return e.message==="re3data: Invalid URL"})) {
        //             validationErrors=[...validationErrors, {type: "warning", message: "re3data: Invalid URL"}]
        //         }
        //     } else {
        //         validationErrors=validationErrors.filter((e)=>{return e.message!="re3data: Invalid URL"})
        //     }
        //     if (metadata.registered.others.url.length>0 && !isValidHttpUrl(metadata.registered.others.url)) {
        //         if (!validationErrors.find((e)=>{return e.message==="Others: Invalid URL"})) {
        //             validationErrors=[...validationErrors, {type: "warning", message: "Others: Invalid URL"}]
        //         }
        //     } else {
        //         validationErrors=validationErrors.filter((e)=>{return e.message!="Others: Invalid URL"})
        //     }
        } else if (currentStep===5) {
            if (metadata.category==="") {
                validationErrors=[...validationErrors, {type: "error", message: "Category is missing"}]
                valid=false;
            }
        }
        return valid
        
        function isValidHttpUrl(input:string) {
            let url;
            
            try {
                url = new URL(input);
            } catch (_) {
                return false;  
            }
            
            return url.protocol === "http:" || url.protocol === "https:";
        }
    }
    
    let validationErrors:{type: "error"|"warning", message: string}[] = [];
    
    async function finishRegistration() {
        if (validatePage()) {
            let resp = await axios.post('/bonsai', metadata, {
                baseURL: $api.base_url+$api.modules.v1
            })
            if (resp.status===200) {
                metadata = {
                    name: "",
                    abbreviation: "",
                    provider: "",
                    areaofapplication: {
                        planning: false,
                        harmonization: false,
                        access: false,
                        discover: false,
                        processing: false,
                        support: false
                    },
                    description: "",
                    inputformats: "",
                    outputformats: "",
                    developmentstage: "",
                    version: "",
                    documentation: "",
                    license: "",
                    link: "",
                    serviceorientation: "",
                    includeincataglog: "",
                    serviceprovidedas: {
                        institutionalMission: {
                            partOf: false,
                            percentage: 0
                        },projectFunding: {
                            partOf: false,
                            percentage: 0
                        },others: {
                            partOf: false,
                            percentage: 0
                        }
                    },
                    funding: "",
                    contact: "",
                    helpdesk: "",
                    supporteduntil: "",
                    technicalbackbone: "",
                    disasterplan: "",
                    entrancecontrol: "",
                    operationstability: "",
                    templates: "",
                    communication: "",
                    registered: {
                        biotools: {
                            registered: false,
                            url: ""
                        },risources: {
                            registered: false,
                            url: ""
                        },eosc: {
                            registered: false,
                            url: ""
                        },fairsharing: {
                            registered: false,
                            url: ""
                        },re3data: {
                            registered: false,
                            url: ""
                        },others: {
                            registered: false,
                            url: ""
                        },
                    },
                    publications: "",
                    category: "",
                    additionalKPI: []
                };
                
                validationErrors=[];
                currentStep = 0;
                steps  = [{
                    active: "step-primary", 
                    title: "General Information"
                }, {
                    active: "", 
                    title: "Organizational Information"
                },{
                    active: "", 
                    title: "Support"
                }, {
                    active: "", 
                    title: "Technical Infrastructure"
                }, {
                    active: "", 
                    title: "Documentation"
                }, {
                    active: "", 
                    title: "Reporting"
                }]   
                
            }
        }
    }
    
</script>

<svelte:head>
<title>Service Registration Form</title>
<meta name="description" content="Biodiversity Onboarding Service Application Form" />
</svelte:head>

<h1 class="flex justify-center text-3xl font-semibold pt-4">BONSAI Form</h1>
<div class="p-4 space-x-2 flex flex-row">
    <div class="w-1/6 min-h-[25rem] bg-base-200 rounded-2xl flex shadow-xl justify-center h-1/3 fixed">
        <ul class="steps steps-vertical">
            {#each steps as step}
            <li class={"step "+step.active} >{step.title}</li>
            {/each}
        </ul>
    </div>
    <div class="min-h-[25rem] flex justify-center min-w-full">
        {#each steps as step, i}
        {#if currentStep===i}
        <UploadCard title={step.title} isFirst={i===0} isLast={i===1}
        on:previous={()=>{if(i!=0){navigate('previous')}}} 
        on:next={()=>{if(i!=5){navigate('next')}}} 
        on:finish={finishRegistration}
        >
        <div slot="card-content">
            {#if i===0}
            <GeneralInformationForm bind:metadata={metadata}/>
            <!-- {:else if i===1} -->
            <!-- coming soon -->
            <!-- <OrganizationalInformationForm bind:metadata={metadata}/> -->
            <!-- {:else if i===2} -->
            <!-- coming soon -->
            <!-- <SupportForm bind:metadata={metadata}/> -->
            <!-- {:else if i===3} -->
            <!-- coming soon -->
            <!-- <TechnicalInfrastructureForm bind:metadata={metadata}/> -->
            <!-- {:else if i===4} -->
            <!-- coming soon -->
            <!-- <DocumentationForm bind:metadata={metadata}/> -->
            <!-- {:else if i===5} -->
            {:else}
            <ReportingForm bind:metadata={metadata}/>
            {/if}
        </div>
    </UploadCard>
    {/if}
    {/each}
</div>
<div class="absolute right-4 space-y-2">
    {#each validationErrors as error}
    <div class="alert alert-{error.type} w-80">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><Warning size={24}/></svg>
        <span>{error.message}</span>
        <button on:click={()=>{validationErrors=validationErrors.filter((e)=>{return e.message!=error.message});}}><Close/></button>
    </div>
    {/each}
</div>
</div>