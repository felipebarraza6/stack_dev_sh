import React from 'react'

import {Card, Tooltip, Tag, Button,  } from 'antd'

import { EyeOutlined, PlusOutlined, OrderedListOutlined } from '@ant-design/icons'

import ModalEnterprise from './ModalEnterprise'

import {getPersons, visibleModalForm } from '../../actions/employess' 

const { Meta } = Card

const CardEnterprise = (attr) =>{
    
    
    return(
        <>
        <Card            
            bordered={true}
            actions={[
                <Tooltip title='Crear persona'>
                    <Button type="primary" onClick={ () => visibleModalForm(attr.dispatch, attr.data)}>
                        <PlusOutlined key ="add_client"/>
                    </Button>
                </Tooltip>,
                <Tooltip title='Datos de empresa'>
                    <Button type="dashed" onClick={ () =>ModalEnterprise(attr.data)}>
                    <EyeOutlined key="profile_enterprise" />
                    </Button>
                </Tooltip>,
                <Tooltip title='Ver personas'>
                    <Button onClick={() =>getPersons(attr.dispatch, 1, attr.data)}>
                        <OrderedListOutlined key="persons" />
                    </Button>
                </Tooltip>,
              ]}
        >   
        
            
            <Meta                
                title={attr.data.name}                
                style={{marginBottom:'0px'}}
                />            
                <div style={{marginTop:'10px', float:'right'}}>
                    <Tag color="processing">{attr.data.type_client}</Tag>
                </div>
                
        </Card>
        </>
    )
}

export default CardEnterprise