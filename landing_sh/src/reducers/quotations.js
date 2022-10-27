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

    case 'SET_CURRENT':
      return {
        ...state,
        steps: {
          ...state.steps,
          current: action.step
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
            finish: action.finish,
            active: action.active,
            hide: action.hide
          }
        } 
    }

    case 'SET_STEP_03':
      return {
        ...state,
        steps: {
          ...state.steps,
          step03: {
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

    default:
      return state
  }

}
