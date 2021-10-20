import { GET_POLYKARPO } from './conifg'


export const getting_list_polykarco = (variable, start_date, end_date, quantity) => {
  
  if (start_date === undefined){
      start_date = ''
  }
  if (end_date === undefined){
      end_date = ''
  }
  const request = GET_POLYKARPO(`data?variable=${variable}&start_date=${start_date}&end_date=${end_date}&qty=${quantity}`)
  return request

}
