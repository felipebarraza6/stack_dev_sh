import axios from 'axios'

const BASE_URL = 'http://localhost:8000/api/'

export const Axios = axios.create({
    baseURL: BASE_URL,
})

export const POST_LOGIN = async (endpoint, data) =>{
    const request = await Axios.post(endpoint, data)
    return request
}
