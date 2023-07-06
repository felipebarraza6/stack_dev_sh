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

const get_profile = async() => {
    const user = JSON.parse(localStorage.getItem('user') || null)
    const rq = await GET(`users/${user.username}/`)    
    return rq.data
}


const downloadFile = async(id_profile, title)=> {
  const now_date = new Date()
  const rq = await DOWNLOAD(`interaction_detail/?profile_client=${id_profile}&created__month=${now_date.getMonth()+1}`, `${title}.xlsx`)
  return rq.data
}

const getDataApiSh = async(id_profile) => {
    const rq = await GET(`interaction_detail_json/?profile_client=${id_profile}&hour=0`)
    return rq.data
}


const sh = {
    authenticated: login,
    billing_data: get_history_data,
    billing_data_admin: get_history_data_admin,
    get_profile: get_profile,
    downloadFile: downloadFile,
    get_data_sh: getDataApiSh
}

export default sh
