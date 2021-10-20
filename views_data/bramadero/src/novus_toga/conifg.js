import axios from 'axios'

const BASE_URL = "https://api.tago.io"


export const INSTANCE_POLYKARPO = axios.create({
  'baseURL': BASE_URL,
  headers: {
      Authorization: '1333aa6c-6a3f-46d0-ab94-6359c6b0cdf3'
  }

})

export const INSTANCE_DITECO = axios.create({
  'baseURL': BASE_URL,
  headers: {
    Authorization: '1333aa6c-6a3f-46d0-ab94-6359c6b0cdf3'
  }
})

export const GET_POLYKARPO = (endpoint) => {
  
  const request = INSTANCE_POLYKARPO.get(endpoint)
  return request

}


