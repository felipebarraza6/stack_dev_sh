import axios from 'axios'


export const BASE_URL = 'http://localhost:8000/api/'
//export const BASE_URL = 'https://api.creanuble.cl'

export const INSTANCE = axios.create({
    baseURL: BASE_URL
})


export const POST = async(endpoints, data) => {        
    const request = await INSTANCE.post(endpoints, data)
    return request
}

export const GET = async(endpoints) => { 
    const request = await INSTANCE.get(endpoints)
    return request
}
