export async function getNovusData1( state, api_novus, setData1, setData2, setData3, setLoad, option){
    
    setLoad(true)
    if(option==0){    
        const rqAcumulado24h = await api_novus.lastDataForHour('3grecdi1va', state.selected_profile.token_service).then((x)=>{
            
            for(var i=0;i<x.length; i++){
                if(x[i+1]){
                    x[i] = {
                        m3: parseFloat(parseInt(x[i+1].m3-parseInt(x[i].m3))/state.selected_profile.scale).toFixed(0), 
                        date:x[i].date
                    }
                }                
            }
            x[0]={
                m3:0,
                date: x[0].date
            }
            x.pop()
            setData1(x)                                    
            setLoad(false)
        }).catch((e)=>{            
            setLoad(false)
        })
    } 
    else if(option==1){
        const rqGetDataMont = await api_novus.getMontData('3grecdi1va', state.selected_profile.token_service).then((x)=>{
            for(var i=0;i<x.length; i++){
                if(x[i+1]){
                    x[i] = {
                        m3: parseInt(parseInt(x[i+1].m3)-parseInt(x[i].m3))/state.selected_profile.scale, 
                        date:x[i].date
                    }
                }                
            }
            x.pop()
            setData2(x)
            setLoad(false)
        }).catch((e)=>{            
            console.log(e)
            setLoad(false)
        })
    } 
    
    else if(option==2){
        const rqNivel = await api_novus.getMontDataLevel(
            state.selected_profile.title=='POZO 3' || state.selected_profile.title=='POZO 2'  ? 
                '3grecuc1v':'3grecuc2v', 
            state.selected_profile.title=='POZO 3'? 
                '321bbb98-4579-4c63-b93f-ecad987b2abf':
                state.selected_profile.title=='POZO 2'? 
                '6c1b1ad5-4103-43a3-b594-bf1e998d094c':
                state.selected_profile.token_service
            ).then((x)=>{
               setData3(x)               
               setLoad(false)
        }).catch((e)=>{
            setLoad(false)  
        })
    } else {
        setData1([])
        setLoad(false)
    }    
    
}