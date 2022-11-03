export const quotation_reducers = (state, action) => {
  
  switch(action.type) {

    case 'SET_CLIENT':
      return {
        ...state,
        client: action.client,
    }
    
    case 'SET_WELLS':
      return {
        ...state,
        wells: action.wells
    }

    case 'SET_VALIDATED_CONTACT':
      return {
        ...state,
        validated_info: {
          ...state.validated_info,
          client_info: true
        }    
      }

    case 'VIEW_WELLS':
      return {
        ...state,
        wells: {
          ...state.wells,
          temporary_well: {
            ...state.wells.temporary_well,
            create_or_edit: false
          }
        }
      }

      case 'NOVIEW_WELLS':
      return {
        ...state,
        wells: {
          ...state.wells,
          temporary_well: {
            ...state.wells.temporary_well,
            create_or_edit: true
          }
        }
      }

    case 'UPDATE_WELL':
      
      state.wells.list.map((x, index)=> {
        
        if(x.general_data.name_well === action.well.general_data.name_well){
          state.wells.list[index]=action.well
        }
      })

      return{
        ...state,        
        wells: {          
          ...state.wells,
          temporary_well:{
            is_edit: false,
            general_data: null,
            well_data: {
              granted_flow: { value:0.0, select:false },
              well_depth:{ value:0.0, select:false },
              static_level:{ value:0.0, select:false },
              dynamic_level:{value:0.0, select:false },
              pump_installation_depth:{ value:0.0, select:false },
              inside_diameter_well:{ value:0.0, select:false },
              duct_outside_diameter:{ value:0.0, select:false },
              has_flow_sensor: { value:null, select:false }
            },
            images: {
              r1: null,
              r2: null
            },
            create_or_edit: true,
            is_load_image: false,
          } 
          }
        }
    
    case 'DELETE_WELL':      
        
      return {
        ...state,
        counter_wells: state.counter_wells-1,
        wells: {
          ...state.wells,
          list: state.wells.list.filter((fruit) => fruit.general_data.name_well !== action.well.general_data.name_well)
          
        }
      }
      

    case 'ADD_WELL_CONFIRM':
      return {
        ...state,
        counter_wells: state.counter_wells+1,
        wells: {
          ...state.wells,
          list: [...state.wells.list, action.well],
          temporary_well:{
            is_edit: false,
            general_data: null,
            well_data: {
              granted_flow: { value:0.0, select:false },
              well_depth:{ value:0.0, select:false },
              static_level:{ value:0.0, select:false },
              dynamic_level:{value:0.0, select:false },
              pump_installation_depth:{ value:0.0, select:false },
              inside_diameter_well:{ value:0.0, select:false },
              duct_outside_diameter:{ value:0.0, select:false },
              has_flow_sensor: { value:null, select:false }
            },
            images: {
              r1: null,
              r2: null
            },
            create_or_edit: true,
            is_load_image: false,
          }
        }
      }

    case 'SELECT_EDIT_WELL':
      return {
        ...state,
        wells: {
          ...state.wells,
          temporary_well: {
            is_edit: true,
            ...action.well,
            general_data: action.well.general_data,          
            well_data: {
              granted_flow: { value:action.well.well_data.granted_flow.value, select:false },
              well_depth:{ value:action.well.well_data.well_depth.value, select:false },
              static_level:{ value:action.well.well_data.well_depth.value, select:false },
              dynamic_level:{ value:action.well.well_data.dynamic_level.value, select:false },
              pump_installation_depth:{ value:action.well.well_data.pump_installation_depth.value, select:false },
              inside_diameter_well:{ value:action.well.well_data.inside_diameter_well.value, select:false },
              duct_outside_diameter:{ value:action.well.well_data.duct_outside_diameter.value, select:false },
              has_flow_sensor: { value:action.well.well_data.has_flow_sensor.value, select:false }
            },
            images: action.well.images,
            create_or_edit: action.well.create_or_edit,
            is_load_image: action.well.is_load_image,
          }          
        }        
      }

    case 'RESET_TEMPORARY_WELL':
      return {
        ...state,
        wells: {
          ...state.wells,
          temporary_well:{
            is_edit: false,
            general_data: null,          
            well_data: {
              granted_flow: { value:0.0, select:false },
              well_depth:{ value:0.0, select:false },
              static_level:{ value:0.0, select:false },
              dynamic_level:{value:0.0, select:false },
              pump_installation_depth:{ value:0.0, select:false },
              inside_diameter_well:{ value:0.0, select:false },
              duct_outside_diameter:{ value:0.0, select:false },
              has_flow_sensor: { value:null, select:false }
            },
            images: {
              r1: null,
              r2: null
            },
            create_or_edit: true,
            is_load_image: false,
          }
        }        
      }

    case 'SET_CURRENT':
      return {
        ...state,
        steps: {
          ...state.steps,
          current: action.step
        }
      }

    case 'SET_IMAGES':
      return {
        ...state,
        wells: {
          ...state.wells,
          temporary_well: {
            ...state.wells.temporary_well,
            images: {
              img1: action.r1,
              img2: action.r2
            }
          }
        }
      }
    
    case 'SET_STEP_01':
      return {
        ...state,
        steps: {
          ...state.steps,
          step01: {
            ...state.steps.step01,
            finish: action.finish,
            active: action.active,
            hide: action.hide
          }
        } 
    }
    case 'SET_STEP_02':
      return {
        ...state,
        steps: {
          ...state.steps,
          step02: {
            ...state.steps.step02,
            finish: action.finish,
            active: action.active,
            hide: action.hide
          }
        } 
    }    
    case 'SET_STEP_03':
      return {
        ...state,
        wells:{
          ...state.wells,
          temporary_well: {
            ...state.wells.temporary_well,
            is_load_image: action.is_load_image
          }
        },
        steps: {
          ...state.steps,
          step03: {
            ...state.steps.step03,
            finish: action.finish,
            active: action.active,
            hide: action.hide
          }
        } 
    }    

    case 'SET_STEP_04':
      return {
        ...state,
        steps: {
          ...state.steps,
          step04: {
            finish: action.finish,
            active: action.active,
            hide: action.hide
          }
        } 
    }

    case 'ADD_GENERAL_DATA':
      return {
        ...state,
        wells: {
          ...state.wells,
          temporary_well: {
            ...state.wells.temporary_well,
            general_data: action.data,
            create_or_edit: false
          }
        }
    }

    case 'CHANGE_CREATE_OR_EDIT':
      return {
        ...state,
        wells: {
          ...state.wells,
          temporary_well: {
            ...state.wells.temporary_well,
            create_or_edit: action.option
          }
        }
      }

    case 'ADD_FIELD_WELL_DATA':
      return{
        ...state,
        wells: {
          ...state.wells,
          temporary_well: {
            ...state.wells.temporary_well,
            well_data: {
              ...state.wells.temporary_well.well_data,
              [action.field]: {
                value:action.value,
                select: action.select
              }
            }
          }
        }
      }



    default:
      return state
  }
}
