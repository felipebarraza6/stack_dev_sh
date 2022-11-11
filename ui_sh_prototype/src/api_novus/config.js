import axios from 'axios'

const BASE_URL = 'https://api.tago.io/data'

// BRAMADERO 1333aa6c-6a3f-46d0-ab94-6359c6b0cdf3
const token_novus = localStorage.getItem('token_novus')
console.log(token_novus)
export const Axios = axios.create({
    baseURL: BASE_URL,
    headers: {
        Authorization: token_novus
    }
})



export const GET = async (endpoint) =>{
    const request = await Axios.get(endpoint)
    return request
}

export const GET_NOT_TOKEN = async(token, endpoint) => {
  const request = axios.get(`${BASE_URL}/${endpoint}`, {
    headers: {
      Authorization: token
    }
  })
  return request
}
