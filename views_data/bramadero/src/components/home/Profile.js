import React, {useReducer, useEffect, useState, useContext } from 'react'

import {Button, Drawer, Row, Col, Divider } from 'antd'
import {UserOutlined} from '@ant-design/icons'

import { reducer } from '../../reducers/profile.js'
import api from '../../api/endpoints'
import { AuthContext } from '../../App'

export const Profile = () =>{

    const userContext = useContext(AuthContext)
    const userData = userContext.state.user
   
    const initialState = {
        loading: true,
        data:  null,
        error: null        
    }

    const [state, dispatch] = useReducer(reducer, initialState)
    const [profile, setProfile] = useState({visible:false})

    const Profile = () =>{
        setProfile({
            visible:true
        })
    }

    const closeProfile = () => {
        setProfile({
            visible: false
        })
    }

    useEffect(() => {

        let isCalled = false

        const fetchData = async() => {

            try{
                const response = await api.user.profile()
                if(!isCalled){
                    dispatch({
                        type: 'GET_PROFILE',
                        loading: false,
                        payload: response
                    })
                }
            }catch(error){
                dispatch({
                    loading: false,
                    error:error.message
                })
            }
        }
        
        fetchData()

        return () => {
            isCalled = true
        }
    }, [])
    
    return (
        <React.Fragment>

            {!state.loading &&
                <Drawer
                    width='400px'
                    visible={profile.visible}
                    onClose={closeProfile}
                    closable={false}
                    title={<><UserOutlined/> {state.data.data.user.email}</>}
                >
                    <Row style={{marginTop:'50px'}}>
                        <Col flex={2}>
                            <p>Usuario</p>
                            <p>Nombre</p>
                            <p>Apellido</p>
                            <p>Email</p>
                        </Col>
                        <Col flex={3}>
                            <p>{state.data.data.user.username}</p>
                            <p>{state.data.data.user.first_name}</p>
                            <p>{state.data.data.user.last_name}</p>
                            <p>{state.data.data.user.email}</p>
                        </Col>
                        <Divider />
                    </Row>

                </Drawer>
            }
            
            <Button onClick={Profile} type='link' style={{color:'white'}}>
            <UserOutlined style={{fontSize:'20px', paddingRight:'5px'}} />
                {userData.email}
            </Button>
        </React.Fragment>
    )
}

export default Profile
