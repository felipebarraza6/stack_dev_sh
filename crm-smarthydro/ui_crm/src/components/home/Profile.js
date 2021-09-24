import React, {useReducer, useEffect, useState } from 'react'

import {Button, Spin, Tooltip, Modal, Table, Tag, notification, Drawer, Row, Col, Divider } from 'antd'
import {BorderlessTableOutlined, UserOutlined, ReloadOutlined, StopOutlined} from '@ant-design/icons'

import { reducer } from '../../reducers/profile.js'
import api from '../../api/endpoints'

//Components
import ModalEnterprise from '../../components/clients/ModalEnterprise'

//Actions
import { viewTask } from '../../actions/tasks'
import { viewPerson } from '../../actions/employess'
import { finishTaskModal } from '../../actions/tasks_dashboard'


export const Profile = () =>{

    const initialState = {
        loading: true,
        data:  null,
        error: null        
    }

    const [state, dispatch] = useReducer(reducer, initialState)

    const columns = [
        {
            title: 'ID',
            dataIndex: 'id',
            key: 'id',
        },
        {
            title: 'Empresa',
            dataIndex: 'client',
            key: 'client',
            render: client => client ? <Button onClick={() => ModalEnterprise(client)} type='primary'>{client.name}</Button> : <StopOutlined />,
        },
        {
            title: 'Cliente',
            dataIndex: 'employee',
            key: 'employee',
            render: employee => employee ? <Button onClick={() => viewPerson(employee)} type='primary'>{employee.name}</Button> : <StopOutlined />
        },
        {
            title: 'Fecha',
            dataIndex: 'date',
            key: 'date',
            render: date =>  date ? <><Tag color="volcano">{date.slice(0,10)}</Tag><Tag color="geekblue">{date.slice(11, 19)} hrs</Tag></> : <StopOutlined />
        },
        {
            title: 'Tarea',
            dataIndex: 'type_action',
            key: 'type action',
            render: type_action => type_action ? <Tag color='processing'>{type_action}</Tag> : <StopOutlined/>
        },
        {
            title: 'Nota',
            dataIndex: 'note',
            key: 'note',
            render: note => note ? <Button onClick={() => Modal.info({ title: `Nota de Tarea`, content: note })} type='dashed'>Nota</Button> : <StopOutlined/>

        },
        { title: '', dataIndex: '', key: 'x', render: task =><> 
            <Button style={{marginRight:'5px'}} onClick={() => viewTask(task)}type='primary'>Ver</Button>            
        
        </>},
        { title: '', dataIndex: '', key: 'x', render: task =><> 
        
        
        <Button 
            type="dashed"
            style={{borderColor:'green', color:'green'}}
            onClick={()=>{
                finishTaskModal(task.id, updateTasks)    
                            
            }

            }
        >
            Completar
        </Button>
    
    </>},
        
    ]

    const ModalTask = () =>{
        Modal.success({
            content: <Table columns={columns} dataSource={state.data.data.actions} pagination={{ pageSize: 3, simple:true}} rowKey='id'></Table>,
            title: `Tareas pendientes de @${state.data.data.user.username}`,
            width: '1220px'
        })
    }

    const updateTasks = async () => {

        try{
            const response = await api.user.profile()
            if(response){
                dispatch({
                    type: 'GET_PROFILE',
                    loading: false,
                    payload: response
                })
                notification.info({
                    message: `Tareas actualizadas!` ,
                    placement: "bottomRight",
                })
            }

        }catch(error){
            dispatch({
                type: 'GET_PROFILE',
                loading: false,
                error: error
            })
        }

    }

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

            <Tooltip title="Actualizar datos">
                <Button onClick={updateTasks} style={{ marginRight:'20px'}} type="link" >
                    <ReloadOutlined />
                </Button>
            </Tooltip>

            <Button onClick={ModalTask} type='primary' style={{marginRight:'15px'}}>
                <BorderlessTableOutlined style={{marginRight:'3px'}} />
                {state.loading ? <Spin/>: state.data.data.actions.length}
                <i style={{paddingLeft:'15px'}}>Tareas Pendientes</i>
            </Button>

            <Button onClick={Profile} type='link' style={{color:'white'}}>
            <UserOutlined style={{fontSize:'20px', paddingRight:'5px'}} />
            {state.loading ? <Spin/>: state.data.data.user.email }
            </Button>
        </React.Fragment>
    )
}

export default Profile