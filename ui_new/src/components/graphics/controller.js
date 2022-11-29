export async function getNovusData1( state, api_novus, setData1, setData2, setData3, setLoad, option){
    
    setLoad(true)
    if(option===0){    
        const rqAcumulado24h = await api_novus.lastDataForHour('3grecdi1va', state.selected_profile.token_service).then((x)=>{
            var listSustraction = []
            for(var i=0; i < x.length; i++){
              if(i>0){
                listSustraction.push({date: x[i].date , 'm3/hora': parseInt((x[i].m3-x[i-1].m3)/state.selected_profile.scale)})

              }
            }
            setData1(listSustraction)                                    
            setLoad(false)
        }).catch((e)=>{            
            setLoad(false)
        })
    } 
    else if(option===1){
        const rqGetDataMonth = await api_novus.getMontData('3grecdi1va', state.selected_profile.token_service).then((x)=>{
            var listSustraction = []
            for(var i=0; i < x.length; i++){
                if(i>0){
                  listSustraction.push({date: `${x[i].date}` , 
                  'm3/dia': x[i-1].m3 < x[i].m3 ? 
                    x[i].m3 - x[i-1].m3 : 
                    (x[i-1].m3+x[i].m3) - x[i-1].m3
                })

            }}
            setData2(listSustraction)
            setLoad(false)
        }).catch((e)=>{            
            console.log(e)
            setLoad(false)
        })
    } 
    
    else if(option===2){
        const rqNivel = await api_novus.getMontDataLevel(
            state.selected_profile.title==='POZO 3' || state.selected_profile.title=='POZO 2'  ? 
                '3grecuc1v':'3grecuc2v', 
            state.selected_profile.title==='POZO 3'? 
                '321bbb98-4579-4c63-b93f-ecad987b2abf':
                state.selected_profile.title==='POZO 2'? 
                '6c1b1ad5-4103-43a3-b594-bf1e998d094c':
                state.selected_profile.token_service
            ).then((x)=>{
                x.pop()
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
