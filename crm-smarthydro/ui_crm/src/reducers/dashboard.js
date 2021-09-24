//Dashboard reducer

export const reducer = (state, action) =>{

    switch (action.type) {
        case 'DASHBOARD_LOADING':
            return{
                ...state,
                loading:true
            }
        case 'TABLE_LOADING':            
            return{
                ...state,
                loading_table:true,
                page: action.page
                
            }

        case 'ACTIVE_FILTER':
            return{
                ...state, filters: {is_active: true, is_priority: false, is_complete: false}
            }
        case 'PRIORITY_FILTER':
            return{
                ...state, filters: {is_active: false, is_priority: true, is_complete: false}
            }
        case 'COMPLETE_FILTER':
            return{
                ...state, filters: {is_active: false, is_priority: false, is_complete: true}
            }
        case 'FALSE_ALL_FILTER':
            return{
                ...state, filters: {is_active: false, is_priority: false, is_complete: false}
            }

        case 'GET_TOTALS':
            return{
                ...state,
                loading: false,
                page: 1,
                loading_table:false,
                totals:{
                    total:action.payload.total.data.count,
                    actives: action.payload.actives.data.count,
                    priority: action.payload.priority.data.count,
                    completes: action.payload.completes.data.count
                },
                quantity: action.payload.total.data.count,
                data: action.payload.total.data.results,

            }

        case 'UPDATE_TOTALS':
            return{
                ...state,
                totals:{
                    total:action.payload.total.data.count,
                    actives: action.payload.actives.data.count,
                    priority: action.payload.priority.data.count,
                    completes: action.payload.completes.data.count,
                    loading_table:false,
                    loading: false,
                }

            }

        case 'GET_DATA':
            return{
                ...state,
                loading: false,
                data: action.payload.data.results,
                quantity: action.payload.data.count,            
                loading_table:false,
                page: action.page
            }

        case 'PAGINATION':
            return{
                ...state,
                loading: false,
                data: action.payload.data.results,
                quantity: action.payload.data.count,
                page:action.page,
                loading_table:false
            }

        case 'ERROR':
            return{
                ...state,
                loading: false,
                error: action.payload
            }

        default:
            return state

    }
}