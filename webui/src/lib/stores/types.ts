export type API = {
    base_url: string,
    modules: {
        aai: string, 
        v1: string
    }
}

export type Token = string

export type ServiceOverview = {
    categories: string[], 
    providers: string[]
}

export type ServiceCategory = {
    name: string,
    description: string
}

export type ServiceProvider = {
    abbreviation: string,
    name: string
}

export type Service = {
    abbreviation: string, 
    name: string, 
    category: string, 
    provider?: string
}

export type ServiceArea = {
    planning: boolean,
    harmonization: boolean,
    access: boolean,
    discover: boolean,
    processing: boolean,
    support: boolean
}
export type ServiceOrientation = "" | "userfacing" | "technical";
export type ServicePartOf = {
    institutionalMission: {
        partOf: boolean,
        percentage: number
    }, projectFunding: {
        partOf: boolean,
        percentage: number
    }, others: {
        partOf: boolean,
        percentage: number
    }
}
export type ServiceRegistration = {
    biotools: {
        registered: boolean,
        url: string
    },risources: {
        registered: boolean,
        url: string
    },eosc: {
        registered: boolean,
        url: string
    },fairsharing: {
        registered: boolean,
        url: string
    },re3data: {
        registered: boolean,
        url: string
    },others: {
        registered: boolean,
        url: string
    }
}

export type Metadata = {
    name: string,
    abbreviation: string,
    provider: string,
    areaofapplication: ServiceArea,
    description: string,
    inputformats: string,
    outputformats: string,
    developmentstage: string,
    version: string,
    documentation: string,
    license: string,
    link: string,
    serviceorientation: ServiceOrientation,
    includeincataglog: string,
    serviceprovidedas: ServicePartOf,
    funding: string,
    contact: string,
    helpdesk: string,
    supporteduntil: string,
    technicalbackbone: string,
    disasterplan: string,
    entrancecontrol: string,
    operationstability: string,
    templates: string,
    communication: string,
    registered: ServiceRegistration,
    publications: string,
    category: string,
    additionalKPI: KPI[]
}

export type Necessity = "mandatory"|"recommended"|"optional"

export type UserDetail = {
    user_name: string, 
    email: string, 
    is_admin: boolean,
    providers: string[]
}

export type KPI = {
    name: string, 
    description: string|null, 
    categories: {
        name: string,
        necessity: Necessity
    }[],
    selected: boolean|undefined
}

export type MeasurementCollector = {
    name?: string, 
    date?: string, 
    [key: string]: number|string|undefined
}

export type Measurement = {
    kpi: string, 
    date: string, 
    value: number|null,
    comment?: string|null
}

export type MeasurementTable = {
    kpis: string[],
    dates: string[],
    results: (number|null)[][],
    comments: (string|null|undefined)[][]
}

export type LineChartData = {
    x: string[], 
    y: (number|null)[], 
    name: string, 
    mode: string, 
    connectgaps: boolean
}[]

export type UserAuthentication = {
    username: string, 
    password: string, 
    email?: string, 
    repeat?: string, 
    remember?: boolean
}

export type MembershipRequest = {
    id: string,
    username: string,
    mail: string,
    provider: string
}

export type RegistrationRequest = {
    user_id: string,
    user_name: string,
    email: string,
    is_admin: boolean|null
}

export type License = {
    reference: string,
    isDeprecatedLicenseId: boolean,
    detailsUrl: string,
    referenceNumber: number,
    name: string,
    licenseId: string,
    seeAlso: string[],
    isOsiApproved: boolean
}