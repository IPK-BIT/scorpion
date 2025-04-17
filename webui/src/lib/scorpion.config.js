export let config = {
    prefix: '',
    domain_name: 'https://scorpion.bi.denbi.de',
    info: {
        title: 'Scorpion',
        description: 'Service Monitoring KPI Dashboard for NFDI'
    },
    aai: {
        register_url: 'https://signup.aai.lifescience-ri.eu/registrar/?vo=lifescience&group=relying_services%3AScorpion',
        oidc: {
            base_url: 'https://login.aai.lifescience-ri.eu'
        },
        image: '/ls-login-button.svg'
    },
    contacts: [
        {
            name: 'Manuel Feser',
            role: 'Software Developer',
            email: 'feser@ipk-gatersleben.de'
        },
        {
            name: 'Uwe Scholz',
            role: 'Principal Investigator',
            email: 'scholz@ipk-gatersleben.de'
        }
    ],
    citation: {
        software: 'Manuel Feser, M. Scorpion [Computer software]. https://github.com/IPK-BIT/scorpion',
        service: 'Feser M and Scholz U. Scorpion enables uniform KPI monitoring of heterogeneous Services within the Biodiversity Community [version 1; not peer reviewed]. F1000Research 2024, 13(ELIXIR):594 (poster) (https://doi.org/10.7490/f1000research.1119738.1)'
    },
    default_profiles: ['nfdi'],
    service_profiles: [
        // {
        //     id: 'denbi',
        //     name: 'de.NBI',
        //     description: 'Metadata profile for de.NBI/ELIXIR-DE',
        //     fields: [
        //         {
        //             type: 'select',
        //             label: 'Service Center', 
        //             required: true, 
        //             options: [
        //                 { value: "BiGi", label: "Bielefeld-Gießen Resource Center for Microbial Bioinformatics" }, 
        //                 { value: "BioInfra.Prot", label: "Bioinformatics Infrastructure for Proteomics" }, 
        //                 { value: "BioData", label: "Center for Biological Data" }, 
        //                 { value: "CIBI", label: "Center for Integrative Bioinformatics" }, 
        //                 { value: "de.NBI-SysBio", label: "de.NBI Systems Biology Service Center" }, 
        //                 { value: "GCBN", label: "German Crop BioGreenformatics Network" }, 
        //                 { value: "HD-HuB", label: "Heidelberg Center for Human Bioinformatics" }, 
        //                 { value: "RBC", label: "RNA Bioinformatics Center" }, 
        //                 { value: "associated", label: "Associated Partners" }
        //             ]
        //         }, 
        //         { 
        //             type: 'url', 
        //             label: 'Service Website', 
        //             pattern: '^(https?://)?([a-zA-Z0-9]([a-zA-Z0-9-].*[a-zA-Z0-9])?.)+[a-zA-Z].*$' 
        //         }
        //     ]
        // }, 
        { 
            id: 'nfdi', 
            name: 'NFDI', 
            description: 'Metadata profile for NFDI', 
            fields: [
                { 
                    type: 'license', 
                    label: 'License',
                    jsonPath: 'license' 
                }, 
                { 
                    type: 'select', 
                    label: 'Development Stage', 
                    jsonPath: 'stage',
                    options: [
                        { value: "dev", label: "Development" }, 
                        { value: "demo", label: "Demonstrator" }, 
                        { value: "prod", label: "Production" }
                    ] 
                }, 
                { 
                    type: 'select', 
                    label: 'Consortia',
                    jsonPath: 'consortia', 
                    multiple: true, 
                    options: [
                        // { value: "base4nfdi", label: "Base4NFDI" }, 
                        // { value: "berd@nfdi", label: "BERD@NFDI" }, 
                        // { value: "daphne4nfdi", label: "DAPHNE4NFDI" }, 
                        // { value: "dataplant", label: "DataPLANT" },
                        // { value: "fairagro", label: "FAIRagro" }, 
                        // { value: "fairmat", label: "FAIRmat" }, 
                        // { value: "ghga", label: "GHGA" }, 
                        // { value: "konsortswd", label: "KonsortSWD" }, 
                        // { value: "mardi", label: "MaRDI" }, 
                        // { value: "nfdi-matwerk", label: "NFDI-MatWerk" }, 
                        { value: "NFDI4Biodiv", label: "NFDI4Biodiversity" }, 
                        // { value: "nfdi4bioimage", label: "NFDI4BIOIMAGE" }, 
                        // { value: "nfdi4cat", label: "NFDI4Cat" }, 
                        // { value: "nfdi4chem", label: "NFDI4Chem" }, 
                        // { value: "nfdi4culture", label: "NFDI4Culture" }, 
                        // { value: "nfdi4datascience", label: "NFDI4DataScience" }, 
                        // { value: "nfdi4earth", label: "NFDI4Earth" }, 
                        // { value: "nfdi4energy", label: "NFDI4Energy" }, 
                        // { value: "nfdi4health", label: "NFDI4Health" }, 
                        // { value: "nfdi4immuno", label: "NFDI4Immuno" }, 
                        // { value: "nfdi4ing", label: "NFDI4Ing" }, 
                        // { value: "nfdi4memory", label: "NFDI4Memory" }, 
                        { value: "NFDI4Micro", label: "NFDI4Microbiota" }, 
                        // { value: "nfdi4objects", label: "NFDI4Objects" }, 
                        // { value: "nfdixcs", label: "NFDIxCS" }, 
                        // { value: "punch4nfdi", label: "PUNCH4NFDI" }, 
                        // { value: "text+", label: "Text+" }
                    ] 
                }
            ] 
        }
    ]
};
