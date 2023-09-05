import { readable, writable, type Readable, type Writable } from "svelte/store";
import type { API, License, ServiceOverview, Token } from "./types";

export const api: Readable<API> = readable(
    {
        base_url: "http://129.70.51.62",
        modules: {
            aai: "/aai",
            v1: "/api/v1"
        }
    }
)

export const token: Writable<Token> = writable("")

export const serviceOverview: Writable<ServiceOverview> = writable({categories: [], providers: []})

export const licenses: Writable<License[]> = writable([])