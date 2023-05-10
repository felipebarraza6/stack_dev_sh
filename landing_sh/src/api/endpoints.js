import { POST, GET, PATCH, INSTANCE } from './config'
import { notification } from 'antd'

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

  const options = {
    headers: {        
        'content-type': 'multipart/form-data'
    }
  }  

  var responses_server = []  

  for(var i = 0; wells.length > i; i++){    
    let data = new FormData()
    data.append('quotation', wells[i].quotation)
    data.append('name', wells[i].general_data.name_well)
    data.append('type_captation', wells[i].general_data.type_captation)
    data.append('exact_address', wells[i].general_data.address_exact)
    data.append('granted_flow', wells[i].well_data.granted_flow.value)
    data.append('well_depth', wells[i].well_data.well_depth.value)
    data.append('static_level', wells[i].well_data.static_level.value)
    data.append('dynamic_level', wells[i].well_data.dynamic_level.value)
    data.append('latitude', wells[i].well_data.latitude)
    data.append('longitude', wells[i].well_data.longitude)
    data.append('pump_installation_depth', wells[i].well_data.pump_installation_depth.value)
    data.append('inside_diameter_well', wells[i].well_data.inside_diameter_well.value)
    data.append('duct_outside_diameter', wells[i].well_data.duct_outside_diameter.value)
    data.append('has_flow_sensor', wells[i].well_data.has_flow_sensor.value)
    if(wells[i].images.r1){
      data.append('img1', wells[i].images.r1)
    }
    if(wells[i].images.r2){
      data.append('img2', wells[i].images.r2)
    }

    const rq = await INSTANCE.post('wells/', data, options).then((response) => {
      notification.success({message: `Pozo "${response.data.name}" creado correctamente`})
    })
    
    responses_server.push(rq)
  }
  return responses_server

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

const create_well = async(data) => {
    const rq = await POST('wells/', data)
    return rq
}

const get_quotation = async(uuid) => {
  const rq = await GET(`quotation/${uuid}/`)
  return rq
}

const update_field = async(id, data)=>{
  const rq = await PATCH(`fields/${id}/`, data)
  return rq
}

const listClients = async()=> {
  const rq = await GET('clients/')
  return rq.data
}




export const callbacks = {
  clients: {
    list: listClients
  },
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
    retrieve: get_quotation,
    create_well: create_well
  }
}
