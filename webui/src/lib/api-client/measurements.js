import { api } from "../../stores/api";
import { get } from "svelte/store";
import axios from "axios";

export async function loadMeasurements(service, start, stop) {
    var page = 0;
    let response = await requestPage(page, service, start, stop);
    let results = response.data.result;
    if (response.data.metadata.totalPages > page +1) {
        for (page = 1; page < response.data.metadata.totalPages; page++) {
            response = await requestPage(page, service, start, stop);
            results = results.concat(response.data.result);
        }
    }
    return results;
}

async function requestPage(page, service, start, stop) {
    const response = await axios.get('/measurements', {
        baseURL: get(api).base_url+get(api).modules.v1,
        params: {
            service: service,
            start: start,
            stop: stop,
            page: page
        }
    })
    return response;
}