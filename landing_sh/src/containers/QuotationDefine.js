import React, { 
  createContext,
  useReducer } from 'react'

import { quotation_reducers } from '../reducers/quotations'
import HeaderDefine from '../components/quotations/HeaderDefine'
import ContainerQuotation from '../components/quotations/ContainerQuotation'

export const QuotationContext = createContext()

const QuotationDefine = () => {
  
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
      current: 0,
      lastCurrent: 0,
      step01: { title: 'Ingresa tus datos de contacto', finish: false, active: true, hide: false },
      step02: { title:'Agregar Pozo', finish: false, active: true, hide: false },
      step03: { title: 'Ingreso exitoso', finish: false, active: false, hide: true },
      step04: { title: 'Resumen y validación', finish: false, active: true, hide: false }
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

  const [state, dispatch] = useReducer(quotation_reducers, initalState)


  return(<QuotationContext.Provider value={{state, dispatch}}>
    <HeaderDefine />
  </QuotationContext.Provider>)

}


export default QuotationDefine
