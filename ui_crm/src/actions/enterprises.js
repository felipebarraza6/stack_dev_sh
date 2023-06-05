
import React from 'react'
import api from '../api/endpoints'

import { Button, notification, Modal, Form, Input, Select } from 'antd'
import { DeleteOutlined, LikeOutlined, UserAddOutlined } from '@ant-design/icons';

const { Option } = Select

export const getTotals = async(dispatch) =>{
    try{
        dispatch({type: 'LOADING'})

        const enterprises = await api.enterprises.get_total_enterprises()

        dispatch({
            type: 'GET_TOTALS',
            payload: enterprises
        })

    }catch(error){
        dispatch({
            type: 'ERROR',
            error:error
        })
    }
}

export const createPerson = async(enterprise)=> {
  //notification.success({message:'Persona creada'})
  
  const onFnish = async(values)=> {
    values = {
      ...values,
      enterprise: enterprise.id
    }
    const rq1 = await api.employess.create_employee(values).then((r)=> {
      Modal.destroyAll()
      notification.success('Persona creada!')
    }).catch((e)=> {
      console.log(e)
    })
    
  }

  Modal.info({okText:'Volver', title:'Crear persona', icon:<UserAddOutlined />, content:<><Form onFinish={onFnish} style={{paddingTop:'30px'}} layout='vertical'>
      <Form.Item label='Nombre' name='name' rules={[{ required: true, message: 'Ingresa el nombre'}]}>
        <Input />
      </Form.Item>
      <Form.Item label='Cargo' name='charge' rules={[{ required: true, message: 'Ingresa el cargo'}]}>
        <Select placeholder='Selecciona un cargo'>
          <Option value="Gerente General">Gerente General</Option>
          <Option value="Gerente de Operaciones">Gerente de Operaciones</Option>
          <Option value="Jefe de Operaciones">Jefe de Operaciones</Option>
          <Option value="Jefe de Planta">Jefe de Planta</Option>
          <Option value="Jefe de Mantención">Jefe de Mantención</Option>
          <Option value="Secretaria General">Secretaria General</Option>
          <Option value="Secretaria administrativa">Secretaria administrativa</Option>
          <Option value="Secretaria Gerencia">Secretaria Gerencia</Option>
          <Option value="Otro Cargo">Otro</Option>
        </Select>
      </Form.Item>
      <Form.Item label='Telefono' name="phone_number" >
        <Input />
      </Form.Item>
      <Form.Item label='Email' name='email' rules={[{ type:"email", required: true, message: 'Ingresa el correo electrónico'}]} >
        <Input />
      </Form.Item>
      <Form.Item>
        <Button style={{float:'right', marginBottom:'-200px'}} htmlType='submit' type='primary'>Crear persona</Button>
      </Form.Item>
    </Form>  

    </>
  })
}

export const updateTotals = async(dispatch) =>{
    try{        

        const enterprises = await api.enterprises.get_total_enterprises()

        dispatch({
            type: 'GET_TOTALS',
            payload: enterprises
        })

    }catch(error){
        dispatch({
            type: 'ERROR',
            payload:error
        })
    }
}

export const getEnterprises = async(dispatch) =>{
    
    dispatch({type: 'LOADING_TABLE'})

    try{    
            
        const enterprises = await api.enterprises.get_enterprises(1)        
    
        dispatch({
            type: 'GET_ENTERPRISES',
            payload: enterprises
        })

    }catch(error){

    }
}

export const getPagination = async(dispatch, page) =>{
    
    try{
        
        dispatch({type:'LOADING_TABLE'})

        const enterprises = await api.enterprises.get_enterprises(page)        

        dispatch({
            type: 'PAGINATION',
            payload: enterprises
        })

    }catch(error){

    }
    

}

export const getRetrieveEnterprise = async(dispatch, id_enterprise) =>{
    
    try{
        dispatch({type: 'LOADING_CONTENT'})
        const enterprise = await api.enterprises.get_retrive_enterprise(id_enterprise)

        dispatch({
            type:'GET_RETRIEVE_ENTERPRISE',
            payload: enterprise.data
        })        
    }catch(error){
        dispatch({type: 'ERROR', error: error})
    }
}

export const postEnterprise = async(dispatch, data) =>{
    
    try{        

        const enterprise = await api.enterprises.create_enterprise(data)    

        dispatch({
            type: 'CREATE_ENTERPRISE',
            payload: enterprise
        })

        getEnterprises(dispatch)

    }catch(error){
        dispatch({
            type: 'ERROR',
            payload: error
        })
    }
}

export const deleteEnterprise = async(dispatch, id_enterprise) =>{
    try{        
        Modal.confirm({
            title:`Eliminar cliente #${id_enterprise}`,
            icon: <DeleteOutlined style={{ color: 'red'}}/>,
            content: `Estas seguro de eliminar el cliente #${id_enterprise}, una vez eliminada no podrás recuperar este registro`,
            okText: 'ELIMINAR',
            okType: 'danger',
            cancelType: 'danger',
            width: '600px',
            onOk: async() =>{
                    const data = await api.enterprises.delete_enterprise(id_enterprise)
                    if(data.status){
                        notification.open({
                            message: `Cliente Eliminado!!`,
                            description: `El cliente #${id_enterprise} fue eliminado`,
                            icon: <DeleteOutlined style={{ color: '#red'}} />
                        })
                        getEnterprises(dispatch)
                    }
            }         
        })

    }catch(error){
        dispatch({type:'ERROR', payload: error})
    }

}

export const updateEnterprise = async(dispatch, id_enterprise, data) =>{
    
    dispatch({type:'LOADING_TABLE'})    

    try{
        const enterprise = await api.enterprises.update_enterprise(id_enterprise, data)
        
                
        dispatch({type: 'UPDATE_ENTERPRISE', payload: enterprise})
        getEnterprises(dispatch)

        notification.open({
            message: `Cliente Actualizado`,
            description: `El cliente #${id_enterprise} fue actualizado correctamente`,
            icon: <LikeOutlined style={{ color: '#1890ff'}} />
        })


    }catch(error){
        console.log({error})
        dispatch({type:'ERROR', payload:error})
    }
}

export const updateStatusEnterprise = async(dispatch, id_enterprise, data) =>{
    
    dispatch({type:'LOADING_TABLE'})

    try{
        const enterprise = await api.enterprises.update_enterprise(id_enterprise, data)
                
        dispatch({type: 'UPDATE_ENTERPRISE', payload: enterprise})
        
        getEnterprises(dispatch)

        updateTotals(dispatch)
    }catch(error){
        Modal.error({content:{error}})
    }
    
}

export const searchEnterprise = async(dispatch, name_enterprise, page) =>{

    try{
        const search = await api.enterprises.search_enterprise(name_enterprise, page)        
        dispatch({type:'FILTER_ENTERPRISE', payload:search})
    }catch(error){
        console.log({error})
    }
}
