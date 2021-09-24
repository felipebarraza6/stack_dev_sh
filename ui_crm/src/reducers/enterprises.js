export const reducer = (state, action) => {

    switch (action.type) {
        case 'LOADING':
            return {
                ...state,
                loading: true
            }

        case 'LOADING_TABLE':
            return {
                ...state,
                loading_table: true
            }

        case 'LOADING_CONTENT':
            return{
                ...state,
                loading_content: true
            }
        
        case 'GET_TOTALS':            
            return {
                ...state,
                loading: false,
                totals: {
                    enterprises: action.payload.enterprises.data.count,
                    enterprises_actives: action.payload.enterprises_actives.data.count,
                    enterprises_inactive: action.payload.enterprises_inactives.data.count
                },
                data: action.payload.enterprises.data.results,
                quantity: action.payload.enterprises_actives.data.count                  
            }

        case 'GET_ENTERPRISES':                        
            return {                
                ...state,                
                loading_table: false,
                data: action.payload.data.results
            }

        case 'GET_RETRIEVE_ENTERPRISE':            
            return{
                ...state,
                loading_content: false,
                enterprise: action.payload,                
            }

        case 'PAGINATION':            
            return{                
                ...state,
                loading: false,                
                data: action.payload.data.results,                
                page:action.page,
                loading_table:false,                
            }

        case 'CREATE_ENTERPRISE':
            return{
                ...state,
                loading: false,
                formData: action.payload,
                error: null
            }

            case 'UPDATE_ENTERPRISE':
                return{
                    ...state,
                    loading_table: false,
                    error: null
                }

        case 'ERROR':            
            return {
                ...state,
                error: action.payload
            }
            
        default:
            return state
    }
}