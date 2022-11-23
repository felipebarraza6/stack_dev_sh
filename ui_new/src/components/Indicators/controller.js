export async function getNovusData1( state, setInd1, setInd2, api_novus){
    
   
    
        const rqGetDataMont = await api_novus.ind1('3grecdi1va', state.selected_profile.token_service).then((x)=>{
            //setInd1(x)
            
            for(var i=0;i<x.length; i++){
                if(x[i+1]){
                    x[i] = {
                        m3: parseFloat(parseInt(x[i].m3-x[i+1].m3)/state.selected_profile.scale).toFixed(0), 
                        date:x[i].date
                    }
                }                
            }
            setInd1(x)
        }).catch((e)=>{            
            console.log(e)
            
        })
    
    
    
   /*     const rqNivel = await api_novus.getMontDataLevel(
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
        })*/
    
    
}