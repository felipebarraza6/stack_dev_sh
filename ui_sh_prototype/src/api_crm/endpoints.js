import { POST_LOGIN, GET, DOWNLOAD  } from "./config"

const login = async(data) =>{
    
    const request = await POST_LOGIN('users/login/', {
        email: data.email,
        password: data.password
    })

    return request.data
}

const get_history_data = async(profile) => {
    const request = await GET(`history_data/?profile=${profile}`)
    return request.data
}

const get_history_data_admin = async() => {
    const request = await GET(`history_data/`)
    return request.data
}

const get_profiles = async() => {
  const rq = await GET('client_profile/')
  return rq.data
}

const get_retrieve = async(user) => {
  const rq = await GET(`users/${user}/`)
  return rq.data
}

const downloadFile = async(id_profile, month)=> {
  const rq = await DOWNLOAD(`interaction_detail/?profile_client=${id_profile}&created__month=${month}`, 'reporte.xlsx')
  return rq.data
}

const api_crm = {
    authenticated: login,
    download_detail: downloadFile,
    billing_data: get_history_data,
    billing_data_admin: get_history_data_admin,
    list_profiles: get_profiles,
    retrieve_user: get_retrieve
}


export default api_crm
