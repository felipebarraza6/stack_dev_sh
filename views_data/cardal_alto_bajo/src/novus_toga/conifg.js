import axios from 'axios'

const BASE_URL = "https://api.tago.io"


export const INSTANCE_POLYKARPO = axios.create({
  'baseURL': BASE_URL,
  headers: {
      Authorization: 'e74a4e2b-f588-45ec-945e-4870832b665d'
  }

})

export const INSTANCE_DITECO = axios.create({
  'baseURL': BASE_URL,
  headers: {
    Authorization: 'e74a4e2b-f588-45ec-945e-4870832b665d'
  }
})

export const GET_POLYKARPO = (endpoint) => {
  
  const request = INSTANCE_POLYKARPO.get(endpoint)
  return request

}

export const GET_DITECO = (endpoint) => {

  const request = INSTANCE_DITECO.get(endpoint)
  return request

}
