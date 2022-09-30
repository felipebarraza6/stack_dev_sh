
import axios from 'axios'

const BASE_URL = 'https://api.smarthydro.cl/api/'
//const BASE_URL = 'http://localhost:8000/api/'


export const INSTANCE = axios.create({
    baseURL: BASE_URL,
})


export const POST_LOGIN = async (endpoint ,data) =>{

    const request = await INSTANCE.post(endpoint, data)

    return request
}

export const GET = async (endpoint) =>{

    const token = JSON.parse(localStorage.getItem('access_token') || null)
    const options = {
        headers: {
            Authorization: `Token ${token}`
        }
    }
    const response = await INSTANCE.get(endpoint, options)

    return response
}

export const POST = async (endpoint, data) =>{

    const token = JSON.parse(localStorage.getItem('access_token') || null)

    const options = {        
        headers: {
            Authorization: `Token ${token}`
        }
    }

    const response = INSTANCE.post(endpoint, data, options)    

    return response
}

export const UPDATE = async (endpoint, data) =>{
    const token = JSON.parse(localStorage.getItem('access_token') || null)

    const options = {        
        headers: {
            Authorization: `Token ${token}`
        }
    }

    const response = INSTANCE.patch(endpoint, data, options)

    return response
}

export const DELETE = async (endpoint) =>{

    const token = JSON.parse(localStorage.getItem('access_token') || null)

    const options = {        
        headers: {
            Authorization: `Token ${token}`
        }
    }

    const response = INSTANCE.delete(endpoint, options)

    return response

}




