

export const reducer = (state, action) => {

    switch (action.type){
        case "GET_PROFILE":
            return {
                ...state,
                loading: false,
                error: null,
                data: action.payload
            }
        case "ERROR":
            return {
                ...state,
                loading: false,
                error: action.payload
            }

        default:
            return state
    }
}