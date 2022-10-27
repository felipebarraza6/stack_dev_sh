import React, { 
  createContext,
  useReducer } from 'react'

import { quotation_reducers } from '../reducers/quotations'
import Header from '../components/quotations/Header'
import ContainerQuotation from '../components/quotations/ContainerQuotation'

export const QuotationContext = createContext()

const QuotationExternalClients = () => {
  
  const initalState = {
    client: null,
    wells: [],
    counter_wells: 0,
    date_now: new Date(),
    steps: { 
      current: 0,
      lastCurrent: 0,
      step01: { title: 'Ingresa tus datos de contacto', finish: false, active: true, hide: false },
      step02: { title:'Agregar Pozo', finish: false, active: true, hide: false },
      step03: { title: 'Imágenes complementarias', finish: false, active: false, hide: true },
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

  console.log(state)

  return(<QuotationContext.Provider value={{state, dispatch}}>
    <Header />
    <ContainerQuotation />
  </QuotationContext.Provider>)

}


export default QuotationExternalClients 
