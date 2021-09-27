
import React from 'react'
import api from '../api/endpoints'
import { Modal, notification, Descriptions } from 'antd'
import { DeleteOutlined, UserOutlined } from '@ant-design/icons';

export const viewPerson = (person) => {
    Modal.info({
        title:<>
            {person.name} 
            </>,
        icon: <UserOutlined style={{ color: '#1890ff'}}/>,
        content: <>                        
            <Descriptions title={'Datos'} bordered style={{marginTop:'20px'}}>
                <Descriptions.Item label="Empresa" span={3}>
                    {person.enterprise}
                </Descriptions.Item>
            
                <Descriptions.Item label="Cargo" span={3}>
                    {person.charge}
                </Descriptions.Item>
            
                <Descriptions.Item label="Email" span={3}>
                    {person.email}
                </Descriptions.Item>
            
                <Descriptions.Item label="Telefono" span={3}>
                    {person.phone_number}
                </Descriptions.Item>
            </Descriptions>
        </>,
        okText: 'OK',
        width: '900px'      
    })

}

export const getTotals = async(dispatch) =>{
    try{
        const employee = await api.employess.get_totals_employees()

        dispatch({
            type: 'GET_TOTALS',
            payload: employee
        })

    }catch(error){
        console.log(error)
    }
}

export const getPersons = async(dispatch, page, enterprise) =>{
  
    dispatch({type: 'LOADING_TABLE'})

    try{

        const employess = await api.employess.get_employess(page, null, enterprise.id)
        dispatch({
            type: 'GET_PERSONS',
            payload: employess.data,
            enterprise: enterprise, 
            page:page
             
        })

    }catch(error){
        console.log({error})
    }
}

export const getEnterprises = async(dispatch, page)=>{        
    dispatch({type:'LOADING_CARDS'})
    try{    
            
        const enterprises = await api.enterprises.get_enterprises(page)        
    
        dispatch({
            type: 'GET_ENTERPRISES',
            payload: enterprises
        })

    }catch(error){

    }
}

export const deletePerson = async(dispatch, person, page, enterprise) =>{
    try{
        Modal.confirm({
            title:`Eliminar Persona`,
            icon: <DeleteOutlined style={{ color: 'red'}}/>,
            content: `Estas seguro de eliminar a ${person.name}, una vez eliminada no podrás recuperar este registro`,
            okText: 'ELIMINAR',
            okType: 'danger',
            cancelType: 'danger',
            width: '600px',
            onOk: async() =>{                
               const data = await api.employess.delete_employee(person.id)
               if(data.status){
                notification.open({
                    message: `Persona Eliminada!`,
                    description: `${person.name} fue eliminado`,
                    icon: <DeleteOutlined style={{ color: '#red'}} />
                })
               }
               getPersons(dispatch, page, enterprise)
            }         
        })
        
    }catch(error){
        console.log(error)
    }
}

export const updatePerson = async(dispatch, person, page, enterprise, data) =>{
    try{        
        const employee = await api.employess.update_employee(person.id, data)
        if(employee.status){
            notification.open({
                message: `Persona Actualizada!`,
                description: `${person.name} fue actualiado`,
                icon: <UserOutlined />
            })
            dispatch({
                type:'OFF_MODAL_UPDATE'
            })
            getPersons(dispatch, page, enterprise)
            getTotals(dispatch)
            
        }
    }catch(error){
        console.log({error})
    }
}

export const createPerson = async(dispatch, data, enterprise, page)=>{
    
    data = {
        ...data,
        "enterprise": enterprise.id
        
    }
    try{
        
        const person = await api.employess.create_employee(data)    
        if(person.status){
            notification.open({
                message: 'Persona creada!',
                description: `${data.name} fue creado`,
                icon: <UserOutlined />
            })
            dispatch({type:'OFF_MODAL_CREATE'})
            getPersons(dispatch, page, enterprise)
            getTotals(dispatch)
        }
    }catch(error){
        console.log({error})
        dispatch({
            type:'ERROR',
            payload: {error}
        })
    }
}

export const visibleModalForm = (dispatch, enterprise) => {    
    dispatch({
        type: 'VISIBLE_MODAL_CREATE',
        enterprise: enterprise
    })
}

export const visibleModalUpdateForm = (dispatch, person) =>{
    dispatch({
        type:'VISIBLE_MODAL_UPDATE',
        person: person
    })
}

export const searchEmployee = async(dispatch, name_employee, page) =>{

    try{
        const search = await api.employess.search_employee(name_employee, page)        
        dispatch({type:'FILTER_EMPLOYEE', payload:search})
    }catch(error){
        console.log({error})
    }
}

