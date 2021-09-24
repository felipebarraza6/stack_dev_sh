import React, { useState, useReducer } from 'react'

import { Form, Button, Modal, Input, Tooltip, Typography, Table } from 'antd'

import {  ApiTwoTone, EditOutlined, DeleteOutlined } from '@ant-design/icons'

//Reducer

import {reducer } from '../../reducers/tasks'

//Actions
import { getTypeTasks, postTypeTasks, deleteTypeTask, updateTypeTask } from '../../actions/tasks'

const { Text } = Typography

const FormTypeTasks = ()=>{

    const [form] = Form.useForm()

    const [modalForm, setModalForm] = useState({
        visible: false
    })

    const initialState = {
        loading: false,
        loading_form: false,
        data:null,
        countTypes:0,
        values: null,
        page: 1

    }

    const [state, dispatch] = useReducer(reducer, initialState)

    const columns = [
        {
            title: 'ID',
            dataIndex: 'id',
            key: 'id'
        },
        {
            title: 'Descripción',
            dataIndex: 'description',
            key: 'description'
        },
        {
            render: (type_task)=><>
                <Tooltip title="Editar">
                    <Button 
                        type="link"
                        onClick={()=> {
                            updateTypeTask(dispatch, type_task, state)
                            
                        }

                        }
                        style={{marginRight: '5px'}}
                        >
                        <EditOutlined style={{fontSize:'20px'}} />
                    </Button>
                </Tooltip>
                <Tooltip title="Eliminar">
                    <Button
                        type="link"
                        onClick={()=> deleteTypeTask(dispatch, type_task, state)}
                        >
                        <DeleteOutlined style={{fontSize:'20px', color:'red'}} />
                    </Button>
                </Tooltip>
                </>
            
        }
    ]

    


    const onFinish = (data) =>{
        
        postTypeTasks(dispatch, data)

        if(postTypeTasks){
            form.resetFields();
        }
    }


    return (
        <React.Fragment>
           
            <Modal
                visible={modalForm.visible}
                title="Tipos de tareas"
                cancelButtonProps={{ style: { display: 'none' } }}
                okButtonProps={{ style: { display: 'none' } }}
                onCancel={()=> setModalForm({...modalForm, visible:false})}
                width={'700px'}                

            >
                <Form
                    form={form}
                    layout="inline"
                    name="form_typetask"
                    style={{marginBottom:'20px'}}
                    initialValues={state.values}
                    onFinish = {onFinish}

                >
                    <Form.Item
                        style={{width:'82%', marginBottom:'10px'}}
                        name="description"
                        rules={[
                            {
                              required: true,
                              message: 'Escribe el nuevo tipo de tarea',
                            },
                          ]}                        
                    >
                        <Input placeholder="Descripción"/>
                    </Form.Item>
                   

                    <Button type="primary" htmlType="submit" >Guardar</Button>

                </Form>
                

                <Table
                    title={() => <><Text strong>TIPOS DE TAREAS ({state.countTypes})</Text></>}
                    columns={columns}
                    dataSource={state.data}
                    rowKey='id'
                    loading = {state.loading}
                    bordered
                    pagination={{                        
                        total:state.countTypes,
                        simple:true,
                        onChange: (page) => getTypeTasks(dispatch, page)
                    }}
                >

                </Table>

            </Modal>

            <Tooltip  title="Tipos de tareas">
                <Button                     
                    type="link" 
                    onClick={
                        () => {setModalForm({
                                ...modalForm, 
                                visible:true
                                })                                                                

                                getTypeTasks(dispatch, 1)
                            }}>
                    <ApiTwoTone style={{fontSize:'30px'}} />
                </Button>
            </Tooltip>
            
            

        </React.Fragment>
    )

}

export default FormTypeTasks