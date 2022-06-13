import { GET } from './config'

const getData = async(variable, start_date, end_date) =>{

    if(!end_date){
        end_date=''
    }
   try {
        const request = await GET(`?variable=${variable}&start_date=${start_date}&end_date=${end_date}&query=last_item`)        
        return request.data        
   } catch(err) {
       console.log(err)
   }
}

const getLastData = async(variable) => {
    try {
        const request = await GET(`?variable=${variable}&query=last_item`)
        return request
    } catch(err) {
        console.log(err)
    }
}


const api_novus = {
    data: getData,
    lastData: getLastData
}


export default api_novus
