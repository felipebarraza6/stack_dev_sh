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

const getLastData = async(variable,token) => {
    try {
        const request = await GET(`?variable=${variable}&query=last_item`, token)
        return request
    } catch(err) {
        console.log(err)
    }
}

const getLastDataHour = async(variable,token) => {
    
    var nowDate = new Date()
    var listData = []

    for(var i =0 ; i < 25; i++){
        
        var date = `${nowDate.getFullYear()}-${nowDate.getMonth()}-${nowDate.getDate()-1}T${i>=10?i:`0${i}`}:00:00`        
        if(i===24){
          date = `${nowDate.getFullYear()}-${nowDate.getMonth()}-${nowDate.getDate()}T00:00:00`        
        }

        const request = await GET(`?variable=${variable}&query=last_item&end_date=${date}`, token)
        console.log(request.data.result[0].value)
        
        listData.push({
            date: i === 24 ? '24 hrs':`${date.slice(11,13)} hrs`,
            m3:request.data.result[0] ? parseInt(request.data.result[0].value) : parseInt(0)
        })                
    }

    
    return(listData)

//    console.log(nowDate.toISOString())
//    console.log(nowDate.setHours(-1))
//    console.log(nowDate.toISOString())

    
}

const getMonth = async(variable,token) => {
    

    var nowDate = new Date()
    var listData = []
    var lastDay = new Date(nowDate.getFullYear(), nowDate.getMonth() + 1, 0)
        

    for(var i =0 ; i < nowDate.getDate(); i++){
        var date = `${nowDate.getFullYear()}-${nowDate.getMonth()}-${i}`        
        if(i==0){
          date = `${nowDate.getFullYear()}-${nowDate.getMonth()-1}-${lastDay.getDate()}`        
        }
        const request = await GET(`?variable=${variable}&query=last_item&end_date=${date}`, token)
        listData.push({
            date:i,
            m3: request.data.result[0] ? 
                    parseInt(request.data.result[0].value):parseInt(0)
        })                
        
    }

    return(listData)


    
}

const getMonthLevel = async(variable,token) => {    
    var nowDate = new Date()
    var listData = []
    for(var i =0 ; i < nowDate.getDate(); i++){        
        var date = `${nowDate.getFullYear()}-${nowDate.getMonth() > 10 ? nowDate.getMonth():`0${nowDate.getMonth()}` }-${nowDate.getDate() > 10 ? i+1:`0${i+1}`}`                
        const request = await GET(`?variable=${variable}&query=last_item&end_date=${date}`, token)

        listData.push({
            date: `${i+1}`,
            'm/dia': request.data.result[0] ? 
                    request.data.result[0].value > 0  && request.data.result[0].value > 50 ? 50.0 :
                request.data.result[0].value
                : 0.0
        })                        
    }    
    return(listData)    
}

const getMonthInd1 = async(variable,token) => {
    var nowDate = new Date()
    var listData = []
    
    nowDate.setDate(nowDate.getDate()-7)

    for(var i =0 ; i < 9; i++){
        
        var date = `${nowDate.getFullYear()}-${nowDate.getMonth()}-${nowDate.getDate()-i}`        
        
        
        const request = await GET(`?variable=${variable}&query=last_item&end_date=${date}`, token)
        
        listData.push({
            date: date,
            m3: request.data.result[0] ? 
                    request.data.result[0].value
                : 0
        })                
        
    }
    
    return(listData)


    
}

const getMonthInd2 = async(variable,token) => {
    var nowDate = new Date()
    var listData = []
    
    nowDate.setDate(nowDate.getDate()-7)

    for(var i =0 ; i < 9; i++){
        
        var date = `${nowDate.getFullYear()}-${nowDate.getMonth()}-${nowDate.getDate()-i}`        
        
        
        const request = await GET(`?variable=${variable}&query=last_item&end_date=${date}`, token)
        
        listData.push({
            date: date,
            mt: request.data.result[0] ? 
                    request.data.result[0].value > 50 ? parseFloat(50): request.data.result[0].value
                : 0
        })                
        
    }
    
    return(listData)


    
}


const api_novus = {
    data: getData,
    lastData: getLastData,
    lastDataForHour: getLastDataHour,
    getMontData: getMonth,
    getMontDataLevel: getMonthLevel,
    ind1: getMonthInd1,
    ind2: getMonthInd2
}


export default api_novus
