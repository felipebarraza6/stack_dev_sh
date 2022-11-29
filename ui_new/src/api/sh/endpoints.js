import { POST_LOGIN, GET, DOWNLOAD_FILE  } from "./config"

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

const get_profile = async() => {
    const user = JSON.parse(localStorage.getItem('user') || null)
    const rq = await GET(`users/${user.username}/`)    
    return rq.data
}

const download = async(profile_id) => {
  const rq = await DOWNLOAD_FILE(`interaction_detail/?profile_client=${profile_id}/`, 'reporte')
  return rq
}

const sh = {
    authenticated: login,
    billing_data: get_history_data,
    billing_data_admin: get_history_data_admin,
    get_profile: get_profile,
    downloadFile: download 
}

export default sh
