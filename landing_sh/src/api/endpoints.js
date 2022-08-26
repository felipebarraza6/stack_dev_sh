import { forwardRef } from 'react'
import { POST, GET } from './config'


const get_fingerprint = async(id) => {
  const request = await GET(`profile_footprints/${id}/`)
  return request
}

const get_webinar = async(id) => {
  const request = await GET(`webinars/${id}/`)
  return request
}


const add_client_external = async(data) => {
  const rq = await POST('clients_external/', data)
  return rq 
}

const create_quotation = async(data) => {
  const rq = await POST('quotation/', data)
  return rq
}

const create_wells = async(wells) => {
  for(var i = 0; wells.length > i; i++){
    const rq = await POST('wells/', wells[i])
    console.log(rq)
  }
  //const rq = await POST('wells/', data)
  //return rq
}


export const callbacks = {
  fingerprint: {
    retrieve: get_fingerprint
  },
  webinar: {
    retrieve: get_webinar
  },
  external_clients: {
    create: add_client_external
  },
  quotation: {
    create: create_quotation,
    createWell: create_wells
  }
     
}
