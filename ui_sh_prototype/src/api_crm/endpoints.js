import { POST_LOGIN, GET  } from "./config"

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

const api_crm = {
    authenticated: login,
    billing_data: get_history_data,
    billing_data_admin: get_history_data_admin,
    list_profiles: get_profiles,
}


export default api_crm
