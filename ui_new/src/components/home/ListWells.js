import React, { useContext } from 'react'
import { Button } from 'antd'
import { AppContext } from '../../App'
import { Row, Col } from 'antd'
import { Link } from 'react-router-dom'

const ListWells = () => {

    const { state, dispatch } = useContext(AppContext)

    return(<Row justify={'center'} style={{padding:'10px'}}>
        {state.profile_client && <>
            {state.profile_client.map((x)=><Col><Button 
                onClick={()=>{
                    dispatch({
                        type:'CHANGE_SELECTED_PROFILE',
                        payload: {
                            selected_profile: x
                        }
                    })
                    
                }}
                key={x.id} type='primary' style={{
                    color: x.id !== state.selected_profile.id ? 'white':'#1F3461',margin:'10px', 
                    backgroundColor: x.id == state.selected_profile.id ? 'white':'#1F3461', 
                    fontSize: x.id == state.selected_profile.id ? '15px':'', 
                    borderColor: '#1F3461', 
                    borderRadius:'5px'}}>{x.title}</Button></Col>)}
        </>}
    </Row>)

}


export default ListWells
