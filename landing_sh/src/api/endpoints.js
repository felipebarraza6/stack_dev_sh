import { POST, GET, PATCH, INSTANCE } from './config'


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
    return rq
  }
}

const get_quotation = async(uuid) => {
  const rq = await GET(`quotation/${uuid}/`)
  return rq
}

const update_field = async(id, data)=>{
  const rq = await PATCH(`fields/${id}/`, data)
  return rq
}

const update_field_file = async(endpoints, file) => {
    const token = JSON.parse(localStorage.getItem('access_token'))
    let data = new FormData()

    data.append('file', file)

    const options = {
      headers: {
          Authorization: `Token ${token}`,
          'content-type': 'multipart/form-data'
      }
    }

    const request = await INSTANCE.patch(endpoints, data, options)
    return request
}


export const callbacks = {
  fingerprint: {
    retrieve: get_fingerprint,
    update_field: update_field,
    update_file: update_field_file

  },
  webinar: {
    retrieve: get_webinar
  },
  external_clients: {
    create: add_client_external
  },
  quotation: {
    create: create_quotation,
    createWell: create_wells,
    retrieve: get_quotation
  }
}
