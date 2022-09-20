import axios from 'axios'
import { notification } from 'antd'
const BASE_URL = 'https://api.smarthydro.cl/api/'
//const BASE_URL = 'http://localhost:8000/api/'
const token = JSON.parse(localStorage.getItem('access_token') || null)

export const Axios = axios.create({
    baseURL: BASE_URL,
})

const download = {
    responseType: 'blob',
    headers: {        
        Authorization: `Token ${token}`
    }
}

export const POST_LOGIN = async (endpoint, data) =>{
    const request = await Axios.post(endpoint, data)
    return request
}


export const GET = async (endpoint) => {
    const token = JSON.parse(localStorage.getItem('access_token'))
    
    const options = {
        headers: {
            Authorization: `Token ${token}`
        }
    }
    const request = await Axios.get(endpoint, options)
    return request
}

export const DOWNLOAD = async(endpoint, name_file) => {
    const request = await Axios.get(endpoint, download).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', name_file)
        document.body.appendChild(link)
        link.click()
    })
    
    notification.open({
        message: 'Notificación de Descarga',
        description: `Archivo ${name_file} descargado...`,
        placement: 'bottomRight'
    })

    return request
}
