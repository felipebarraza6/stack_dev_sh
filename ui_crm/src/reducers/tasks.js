
export const reducer = (state, action) => {

    switch (action.type) {

        case 'LOADING':
            return{...state, loading: true}

        case 'LOADING_TOTALS':
            return{...state, loadingTotals: true}
        case 'LOADING_ACTIVES':
            return{...state, loadingActives: true}
        case "LOADING_PRIORITIES":
            return{...state, loadingPriority: true}
        case "LOADING_COMPLETES":
            return{...state, loadingCompletes: true}
        case "LOADING_TABLES":
            return{...state, loadingTotals:true, loadingActives:true, loadingPriority:true, loadingCompletes:true}

        case "LOADING_TYPES":
            return{...state, loading: true}
        case "LOADING_FORM":
            return{...state, loading_form: true}
     
        case 'RELOAD_ALL_DATA':
           return{
                ...state,

                totalsData: action.payload.totals.data.results,
                activesData: action.payload.actives.data.results,
                priorityData: action.payload.priority.data.results,
                completesData: action.payload.completes.data.results,

                countTotals: action.payload.totals.data.count,
                countActives: action.payload.actives.data.count,
                countPriority: action.payload.priority.data.count,
                countCompletes: action.payload.completes.data.count,

                totals: action.payload,
                loading: false,

                loadingTotals:false,
                loadingActives:false,
                loadingPriority:false,
                loadingCompletes:false,

                date_range:{
                    start_date:action.payload.date_range.start_date,
                    end_date:action.payload.date_range.end_date
                },
                year:action.payload.year,
                month:action.payload.month,
                day:action.payload.day,

                id_enterprise_selected:action.payload.id_enterprise_selected,
                id_person_selected:action.payload.id_person_selected

            }

        case 'PAGINATION_TOTALS':            
            return{
                ...state,
                pageTotals: action.page,
                loadingTotals: false,
                totalsData: action.payload.data.results
            }

        case 'PAGINATION_ACTIVES':
            return{
                ...state,
                pageActives: action.page,
                loadingActives: false,
                activesData: action.payload.data.results
            }

        case 'PAGINATION_PRIORITIES':
            return{
                ...state,
                pagePriority: action.page,
                loadingPriority: false,
                priorityData: action.payload.data.results
            }
        
        case 'PAGINATION_COMPLETES':            
            return{
                ...state,
                pageCompletes: action.page,
                loadingCompletes: false,
                completesData: action.payload.data.results
            }

        case 'GET_TYPE_TASKS':
            return{
                ...state,
                loading: false,
                data: action.payload.data.results,
                countTypes: action.payload.data.count,
                page:action.page
            }

        case 'VALUES_FORM':
            return{
                ...state,
                values:action.payload,
                loading_form: false
            }

        
        case 'CLEAN_RANGE_DATE':
            return {
                ...state,
                date_range:{
                    start_date:'',
                    end_date:''
                },
                year:'',
                month:'',
                day:''
            }
        
        case 'CLEAN_IDS_SELECTED':
            return{
                ...state,
                id_enterprise_selected:'',
                id_person_selected:''

            }
        
        case 'FILTER_ENTERPRISE':
            return{
                ...state,
                filter_enterperises: action.payload.data.results
            }
        
        case 'ENTERPRISE_SELECTED':
            return{
                ...state,
                id_enterprise_selected: action.value
            }

        case 'FILTER_EMPLOYEE':
            return{
                ...state,
                filter_employees: action.payload.data.results
            }

        case 'PERSON_SELECTED':
            return{
                ...state,
                id_person_selected: action.value
            }
            
        default:
            return state


    }

}