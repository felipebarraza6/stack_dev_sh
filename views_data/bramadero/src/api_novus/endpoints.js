import { GET } from './config'

const getData = async(variable, start_date, end_date, qty) =>{
   try {
        const request = await GET(`?variable=${variable}&start_date=${start_date}&end_date=${end_date}&qty=${qty}`)
        return request.data
   } catch(err) {
       console.log(err)
   }
}


const api_novus = {
    data: getData,
}


export default api_novus
