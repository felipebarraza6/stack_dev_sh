
export const login_reducer = (state, action) => {

    switch (action.type) {

        case "LOGIN":

            localStorage.setItem("access_token", JSON.stringify(action.payload.access_token))
            localStorage.setItem("user", JSON.stringify(action.payload.user))
            return {
                ...state,
                isAuthenticated: true,                
                access_token: action.payload.access_token,
                user: action.payload.user
            }
            
        case "LOGOUT":
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