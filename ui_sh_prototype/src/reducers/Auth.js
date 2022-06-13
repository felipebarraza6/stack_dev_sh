export const reducer = (state, action) => {
    switch (action.type) {

        case 'LOGIN_A':

            localStorage.setItem("access_token", JSON.stringify(action.payload.access_token))
            localStorage.setItem("user", JSON.stringify(action.payload.user))            
            localStorage.setItem("token_novus", localStorage.getItem('token_novus'))
            var data_ad = JSON.parse(localStorage.getItem('data_p'))
            localStorage.setItem("data_p", JSON.stringify({
              "d1": data_ad.d1,
              "d2": data_ad.d2,
              "d3": data_ad.d3,
              "d4": data_ad.d4,
              "d5": data_ad.d5,
              "d6": data_ad.d6
            }))


            return {
                ...state,
                isAuthenticated: true,                
                access_token: action.payload.access_token,
                user: action.payload.user
            }
 

        case 'LOGIN':
            localStorage.setItem("access_token", JSON.stringify(action.payload.access_token))
            localStorage.setItem("user", JSON.stringify(action.payload.user))            
            localStorage.setItem("token_novus", action.payload.user.profile_data.token_service)
            localStorage.setItem("data_p", JSON.stringify({
              "d1": action.payload.user.profile_data.d1,
              "d2": action.payload.user.profile_data.d2,
              "d3": action.payload.user.profile_data.d3,
              "d4": action.payload.user.profile_data.d4,
              "d5": action.payload.user.profile_data.d5,
              "d6": action.payload.user.profile_data.d6
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
