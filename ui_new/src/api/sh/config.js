import axios from 'axios'

const BASE_URL = 'https://api.smarthydro.cl/api/'
//const BASE_URL = 'http://localhost:8000/api/'

export const Axios = axios.create({
    baseURL: BASE_URL,
})



export const POST_LOGIN = async (endpoint, data) =>{
    const request = await Axios.post(endpoint, data)
    return request
}


export const GET = async (endpoint) => {
    const token = JSON.parse(localStorage.getItem('token'))
    
    const options = {
        headers: {
            Authorization: `Token ${token}`
        }
    }
    const request = await Axios.get(endpoint, options)
    return request
}
export const DOWNLOAD_FILE = async(endpoint, name_file) => {
    const token = JSON.parse(localStorage.getItem('token'))
    const options = {
        responseType: 'blob',
        headers: {
            Authorization: `Token ${token}`
        }
    }
    axios({
      url: `https://api.smarthydro.cl/api/${endpoint}`,
      headers: {
        Authorization: `Token ${token}`,
      },
      method: 'GET',
      responseType: 'blob', // important
    }).then((response) => {
      console.log('response', response)
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'file.pdf');
      document.body.appendChild(link);
      link.click();
    }).catch((x)=>console.log(x))
}
