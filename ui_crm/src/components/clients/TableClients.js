import React from 'react'

import { Table, Button, Tooltip, Typography, Descriptions } from 'antd'
import { DeleteOutlined, EditOutlined , LikeOutlined, DislikeOutlined } from '@ant-design/icons'

import {deletePerson, getPersons, updatePerson, visibleModalUpdateForm } from '../../actions/employess'

const { Text } = Typography

const TableClients = (attr) =>{
    
    const columns = [        
        
        {
            title:'Nombre',
            dataIndex: 'name',
            key: 'name'
        },
        {
            title:'Acciones',
            key: 'id',
            render: (person) =>   <> 
                            <Tooltip title='Editar persona'>
                                <Button type="link" onClick={()=> {visibleModalUpdateForm(attr.dispatch, person)}}>
                                    <EditOutlined style={{color:'#1890ff'}}/>
                                </Button>
                            </Tooltip>                                                        
                            {person.is_active ? 
                            
                            <Tooltip title='Establecer como inactivo'>
                                <Button type="link" onClick={() => {updatePerson(attr.dispatch, person, attr.page, attr.enterprise, {is_active: false})}} >
                                    <LikeOutlined style={{color:'#1890ff'}}/>
                                </Button>
                            </Tooltip> :
                            <Tooltip title='Establecer como activo'>
                            <Button type="link" onClick={() => {updatePerson(attr.dispatch, person, attr.page, attr.enterprise, {is_active: true})}} >
                                <DislikeOutlined style={{color:'red'}}/>
                            </Button>
                            </Tooltip> 
                            }
                            <Tooltip title='Eliminar persona'>
                                <Button onClick={() => {deletePerson(attr.dispatch, person, attr.page, attr.enterprise)}} type="link">
                                    <DeleteOutlined style={{color:'red'}}/>
                                </Button>
                            </Tooltip>                             
                            </>            
        }
    ]

    const expandedRowRender = (person) => {
        return(
            <Descriptions layout="vertical">                
                <Descriptions.Item label="Telefono">{person.phone_number ? person.phone_number : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="Cargo">{person.charge ? person.charge : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="Empresa">{person.enterprise ? person.enterprise : 'S/D'}</Descriptions.Item>
                <Descriptions.Item span={3} label="Email">{person.email ? person.email : 'S/D'}</Descriptions.Item>                
            </Descriptions>
        )
    }

    return(        
                        
        <Table
        columns={columns}        
        dataSource={attr.data}
        loading={attr.loading}
        rowKey='id'
        title={() => 
            <React.Fragment>
                {attr.enterprise ? 
                    <Text mark >{attr.enterprise.name} ({attr.quantity})</Text> : <Text mark>TODOS({attr.quantity})</Text>
                } 
                <Button type="primary" onClick={() => getPersons(attr.dispatch, 1, '')} style={{float: 'right'}}>TODOS</Button>                
            </React.Fragment>
            }
        pagination={{            
            total: attr.quantity,
            simple:true,
            current: attr.page,
            onChange: page => {getPersons(attr.dispatch, page, attr.enterprise)} 
        }}
        expandable={{ expandedRowRender }}
        
        />
        
    )
}

export default TableClients