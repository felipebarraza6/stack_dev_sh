import { GET, POST_LOGIN } from './api'

const login = async (data) => {

    const request = await POST_LOGIN('users/login/', {
        email: data.email,
        password: data.password
    })

    return request.data
}

const profile = () =>{

    const user_local = JSON.parse(localStorage.getItem('user') || null)
    const request = GET(`users/${user_local.username}/`)

    return request

}





const api = {
    user:{
        login,
        profile
    }
}

export default  api