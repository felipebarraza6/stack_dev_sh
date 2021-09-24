import React, { useState } from 'react'

import {  Button, Modal, Tooltip, Form, Input, 
        DatePicker, Select, notification, Checkbox } from 'antd'
import { BookTwoTone } from '@ant-design/icons'

import { PlusCircleTwoTone } from '@ant-design/icons'

import api from '../../api/endpoints'

import moment from 'moment'

//Actions
import { reloadTasks } from '../../actions/tasks'

const { TextArea } = Input
const { Option } = Select

const FormTask = ({ dispatch })=>{

    const [modalForm, setModalForm] = useState({
        visible: false
    })

    const [formTask, setFormTask] = useState({
        type_actions:null,
        enterprises:null,
        persons:null
    })

    const getTypeTask = async(value)=>{

        const type_actions =  await api.type_tasks.search_type_task(value)        
        setFormTask({
            ...formTask, 
            type_actions:type_actions.data.results,
            status_person:true
        })
    }

    const getEnterprises = async(value) =>{
        const enterprises = await api.enterprises.search_enterprise(value)
        setFormTask({
            ...formTask,
            enterprises:enterprises.data.results
        })
    }

    const getPersons = async(id_enterprise) =>{
        const persons = await api.enterprises.get_retrive_enterprise(id_enterprise)        
        setFormTask({
            ...formTask,
            persons:persons.data.employess
        })
    }

    const createTask = async(values) =>{
        
        values = {
            ...values,
            'date':moment(values.date)
        }
        if(values.is_complete){
            values = {
                ...values,
                'date_complete':moment(values.date),
                'is_active':false,
                'is_priority':false
            }
        }
        

        const task = await api.tasks.create_task(values)

        if(task.status){
            
            form.resetFields()
            
            reloadTasks(dispatch, {totals:1, actives:1, priorities:1, completes:1})    
            
            setModalForm({
                ...modalForm,
                visible:false
            })

            notification.open({
                message: 'Tarea Creada!',
                description: `Nueva tarea creada`,
                icon: <BookTwoTone />
            })

        }        

        setFormTask({
            type_actions:null,
            enterprises:null,
            persons:null
        })

    }

    const [form] = Form.useForm()


    return (
        <React.Fragment>
            <Modal
                visible={modalForm.visible}
                title="NUEVA TAREA"
                okText="Crear Tarea"
                cancelText="Cancelar"
                onCancel={()=> setModalForm({...modalForm, visible:false})}
                width={'400px'}
                onOk={() => {
                    form
                      .validateFields()
                      .then(values => {
                        createTask(values)
                      })
                      .catch(info => {
                        console.log('Validate Failed:', info)
                      })
                  }}
            >
                <Form
                    form={form}
                    name="form_task"
                    layout="vertical"
                    style={{marginBottom:'20px'}}
                    onFinish = {(values)=>console.log(values)}
                >   
                    <Form.Item name="type_action" label="Tipo de Tarea" rules={[{required: true,message: 'Escribe el nuevo tipo de tarea',}]}>
                        <Select 
                            showSearch
                            placeholder="Busca un tipo de tarea"
                            optionFilterProp="children"
                            notFoundContent={'No se encuentra'}
                            onSearch={(value)=>{

                                getTypeTask(value)
                            }} 
                        >
                            {formTask.type_actions &&
                            formTask.type_actions.map((option, index)=> (
                            <Option key={index} value={option.id}>{option.description}</Option>
                            )

                    )}
                        </Select>
                    </Form.Item>

                    <Form.Item name="client" label="Empresa" rules={[{required: true,message: 'Selecciona una empresa',}]}>
                        <Select
                            showSearch
                            placeholder="Busca una empresa"
                            optionFilterProp="children"
                            notFoundContent={'No se encuentra'} 
                            onSearch={(value)=>{

                                getEnterprises(value)
                            }} 
                            onSelect={(value)=>{
                                getPersons(value)
                            }}
                            
                        >
                            {formTask.enterprises &&
                            formTask.enterprises.map((option, index)=> (
                                    <Option key={index} value={option.id}>{option.name}</Option>
                                )
                            )}

                        </Select>
                    </Form.Item>

                    <Form.Item name="employee" label="Persona" rules={[{required: true,message: 'Debes seleccionar una persona',}]}>
                        <Select                     
                            placeholder="Selecciona una persona"
                            optionFilterProp="children"
                            notFoundContent={'Selecciona una empresa'} 
                            
                        >
                            {formTask.persons &&
                            formTask.persons.map((option, index)=> (
                                    <Option key={index} value={option.id}>{option.name}</Option>
                                )
                            )}  
                        </Select>
                    </Form.Item>

                    <Form.Item name="date" label="Fecha de ejecución" rules={[{required: true,message: 'Selecciona una fecha',}]}>
                        <DatePicker style={{width:'100%'}} showTime={{ format: 'HH:mm:ss' }} />
                    </Form.Item>
                    
                    <Form.Item name="is_complete" valuePropName="checked">
                        <Checkbox>ACCION COMERCIAL</Checkbox>
                    </Form.Item>
                    

                    <Form.Item name="note" label="Nota">
                        <TextArea rows={4} />
                    </Form.Item>                    
                </Form>

            </Modal>
            <Tooltip  title="Nueva tarea">
            <Button type="link" onClick={() => setModalForm({...modalForm, visible:true})}>
                <PlusCircleTwoTone style={{fontSize:'30px'}} />
            </Button>
            </Tooltip>
        </React.Fragment>
    )

}

export default FormTask