import { api } from "../../stores/api";
import { get } from "svelte/store";
import axios from "axios";

export async function loadServices(params) {
    var page = 0;
    let response = await requestPage(page, params);
    let results = response.data.result;
    if (response.data.metadata.totalPages > page+1) {
        for (let i = page+1; i < response.data.metadata.totalPages; i++) {
            response = await requestPage(i, params);
            results = results.concat(response.data.result);
        }
    }
    return results;
}

async function requestPage(page, parameters) {
    var params = {
        page: page,
        ...parameters
    }
    const response = await axios.get('/services', {
        baseURL: get(api).base_url+get(api).modules.v1,
        params: params
    })
    
    try {
        return response
    } catch (error) {
        console.error(error)
    }
}