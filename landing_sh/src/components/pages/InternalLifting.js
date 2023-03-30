import React, { 
    createContext,
    useReducer } from 'react'
  
  import { internal_lifting_reducers } from '../../reducers/internal_lifting'
  import Header from '../internal_lifting/Header'
  import ContainerInternalLifting from '../internal_lifting/ContainerInternalLifting'
  import { Row, Col } from 'antd'
  
  export const InternalLiftingContext = createContext()
  
  const InternalLifting = ({ match }) => {
    
    var id_person = null
    
    if(match){
      id_person = match.params.id
    }
  
    console.log(id_person)
    const initalState = {
      client: null,
      wells: { 
        list:[],
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
        },      
      },
      counter_wells: 0,
      date_now: new Date(),
      steps: { 
        current: match ? 1: 0,
        lastCurrent: 0,
        step01: { title:'Agregar Pozo', finish: false, active: true, hide: false },
        step02: { title: 'Ingreso exitoso', finish: false, active: false, hide: true },
        step03: { title: 'Resumen y validación', finish: false, active: true, hide: false },
        step04: { title: 'Selecciona al cliente', finish: false, active: true, hide: false },
      },
      validated_info: {
        client_info: false,
        wells_info: {
          general: false,
          detail: false,
          add_image:false
        },
        process_info: false
      }   
    }
  
    const [state, dispatch] = useReducer(internal_lifting_reducers, initalState)
  
  
    return(<InternalLiftingContext.Provider value={{state, dispatch}}>
      
            <ContainerInternalLifting />
    </InternalLiftingContext.Provider>)
  
  }
  
  
  export default InternalLifting
  