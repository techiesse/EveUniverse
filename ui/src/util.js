export async function fetchJson(url){
    const response = await fetch(url)
    const jsonResponse = await response.json()
    return jsonResponse
}

export async function fetchResource(url){
    const jsonResponse = await fetchJson(url)
    return jsonResponse.data
}

export async function fetchTrackingList(name){
    return await fetchResource(`http://localhost:8000/main/api/tracking-list/1/${name}/`)
    //const response = await fetch(`http://localhost:8000/api/tracking-list/1/${name}/`)
    //const jsonResponse = await response.json()
    //return jsonResponse.data
}
