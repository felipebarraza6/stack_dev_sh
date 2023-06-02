export async function getNovusData(setCaudal, setNivel, state, api_novus, setAcumulado, acumulado, nivel){
    const rqCaudal = await api_novus.lastData(state.selected_profile.title=='POZO 2' ?'3grecuc2v': 
      state.selected_profile.title=='Las Pircas' ? '3grecuc2v': 
      state.selected_profile.title=='PAINE' ? 'wifia1va':
      state.user.id==32 ? '3grecuc2v':state.user.id==34 ? '3grecuc2v':
      '3grecuc1v', state.selected_profile.token_service).then((x)=>{
        if(x.data.result[0].value > 0){
            setCaudal(x.data.result[0].value)
        } else{
            setCaudal(0.0) 
        }
        
    }).catch((e)=>{
            setCaudal(0.0)
    })    
    const rqNivel = await api_novus.lastData(
        state.selected_profile.title=='POZO 3' || state.selected_profile.title=='POZO 2'  ? '3grecuc1v': 
        state.selected_profile.title=='Las Pircas' ? '3grecuc1v': state.selected_profile.title=='PAINE' ? 'wifia2va':
        state.user.id==32 ? '3grecuc1v':state.user.id==34?'3grecuc1v':'3grecuc2v', 

        state.selected_profile.title=='POZO 3'? 
            '321bbb98-4579-4c63-b93f-ecad987b2abf':
            state.selected_profile.title=='POZO 2'? 
            '6c1b1ad5-4103-43a3-b594-bf1e998d094c':
            state.selected_profile.token_service
        ).then((x)=>{
            if(x.data.result[0].value > 0){ 
                setNivel(x.data.result[0].value)
            } else{
                setNivel(0.0)
            }                    
    }).catch((e)=>{
        setNivel(0.0)  
    })
    const rqAcumulado = await api_novus.lastData('3grecdi1va', state.selected_profile.token_service).then((x)=>setAcumulado(
        parseInt(x.data.result[0].value / state.selected_profile.scale)
    )).catch((e)=>{
        setAcumulado(0)  
    })
    return{
        rqCaudal,
        rqNivel,
        rqAcumulado
    }
}
