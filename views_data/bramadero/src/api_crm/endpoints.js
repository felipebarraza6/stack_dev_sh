import { POST_LOGIN  } from "./config"

const login = async(data) =>{
    
    const request = await POST_LOGIN('users/login/', {
        email: data.email,
        password: data.password
    })

    return request.data
}


const api_crm = {
    authenticated: login
}


export default api_crm