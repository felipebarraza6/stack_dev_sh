export const reducer = (state, action) => {
    switch (action.type) {

        case 'LOGIN_A':
            localStorage.setItem("access_token", JSON.stringify(action.payload.access_token))
            localStorage.setItem("user", JSON.stringify(action.payload.user))            
            localStorage.setItem("token_novus", localStorage.getItem('token_novus'))
            localStorage.setItem("selected_sensor", localStorage.getItem('selected_sensor'))
            var data_ad = JSON.parse(localStorage.getItem('data_p'))
            localStorage.setItem("data_p", JSON.stringify({
              "d1": data_ad.d1,
              "d2": data_ad.d2,
              "d3": data_ad.d3,
              "d4": data_ad.d4,
              "d5": data_ad.d5,
              "d6": data_ad.d6
            }))
            let user = action.payload.user
            console.log(action.payload.update_data)
            user = {
              ...user,
              'profile_data': action.payload.update_data.sensors[0].profile_data
            }

            localStorage.setItem("user", JSON.stringify({...user, "profile_data": action.payload.update_data.sensors[0].profile_data}))

            return {
                ...state,
                isAuthenticated: true,                
                access_token: action.payload.access_token,
                user: user
            }
 

        case 'LOGIN':
            localStorage.setItem("access_token", JSON.stringify(action.payload.access_token))
            localStorage.setItem("user", JSON.stringify(action.payload.user))            
            localStorage.setItem("token_novus", action.payload.user.profile_data[0].token_service)
            localStorage.setItem("selected_sensor", JSON.stringify(action.payload.user.profile_data[0]))
            localStorage.setItem("data_p", JSON.stringify({
              "d1": action.payload.user.profile_data[0].d1,
              "d2": action.payload.user.profile_data[0].d2,
              "d3": action.payload.user.profile_data[0].d3,
              "d4": action.payload.user.profile_data[0].d4,
              "d5": action.payload.user.profile_data[0].d5,
              "d6": action.payload.user.profile_data[0].d6
            }))


            return {
                ...state,
                isAuthenticated: true,                
                access_token: action.payload.access_token,
                user: action.payload.user
            }

        case 'LOGOUT':
            localStorage.clear()
            return {
                ...state,
                isAuthenticated: false,
                access_token: null,
                user: null
            }
        
        default:
            return state
    }
}
