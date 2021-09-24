
export const reducer = (state, action) =>{

    switch (action.type) {
        
        case "LOADING":
            return{...state,loading:true}
        case "LOADING_CARDS":
            return{...state,loading_cards:true}
        case "LOADING_TABLE":
            return{...state,loading_table:true}

        case "GET_ENTERPRISES":
            return{
                ...state,
                loading_cards:false,
                enterprises: action.payload.data
            }        

        case "GET_TOTALS":            
            return{
                ...state,
                totals:action.payload,
                loading:false
            }
            
        case 'GET_PERSONS':
            return{
                ...state,
                loading_table: false,
                dataClients:action.payload.results,
                quantity_persons: action.payload.count,
                enterprise_selected: action.enterprise,
                pageTable: action.page
            }

        case 'VISIBLE_MODAL_CREATE':            
            return{
                ...state,
                modalFormVisible: true,
                enterpriseModal: action.enterprise
            }                
        
        case 'OFF_MODAL_CREATE':
            return{
                ...state,
                modalFormVisible: false,
                error:null                 
            }

        case 'VISIBLE_MODAL_UPDATE':
            return{
                ...state,
                modalUpdateVisible: true,
                personModal: action.person
            }

        case 'OFF_MODAL_UPDATE':
            return{
                ...state,
                modalUpdateVisible: false,
                error:null
            }

        case "ERROR":            
            return{
                ...state,
                error: action.payload.error.response.data
            }

        default:
            return state
    }

}