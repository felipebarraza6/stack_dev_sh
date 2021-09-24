import React from 'react'

import {Table, Button, Tooltip } from 'antd'

import { EditOutlined, DeleteOutlined, LikeTwoTone, DislikeTwoTone } from '@ant-design/icons'

import { deleteEnterprise, updateStatusEnterprise, getRetrieveEnterprise } from '../../actions/enterprises'

import ModalEnterprise from '../../components/clients/ModalEnterprise'

const ListClients = (enterprises) =>{      
      
      const columns = [
        {
          title: 'ID',
          dataIndex: 'id',
          key: 'id',
        },
        {
          title: 'Empresa',
          render: (item) =><Tooltip title="Ver Perfil">
                              <Button onClick={() =>{ ModalEnterprise(item) }} type="primary">{item.name}</Button>                                    
                            </Tooltip>
        },
        {
          title: 'Tipo',
          dataIndex: 'type_client',
          key: 'type_client'
        },
        {
          title: 'Comuna',
          dataIndex: 'commune',
          key: 'commune'
        },
        {                 
          render: (item) => <>
                              <Tooltip title="Editar">
                                <Button onClick={() => getRetrieveEnterprise(enterprises.dispatch,item.id)} type="link"><EditOutlined style={{ fontSize: '20px' }}/></Button>
                              </Tooltip>
                              <Tooltip title="Eliminar">
                                <Button onClick={() => deleteEnterprise(enterprises.dispatch, item.id)} type="link"><DeleteOutlined style={{ color:'red', fontSize: '20px' }}/></Button>
                              </Tooltip>
                              {!item.is_active ?                             
                                <Tooltip title="Establecer como Activo">
                                    <Button onClick={() => updateStatusEnterprise(enterprises.dispatch, item.id, {'is_active': true})} type="link"><DislikeTwoTone twoToneColor="#eb2f96" style={{ fontSize: '20px' }}/></Button>
                                </Tooltip>
                              :
                                <Tooltip title="Establecer como Inactivo">
                                  <Button onClick={() => updateStatusEnterprise(enterprises.dispatch, item.id, {'is_active': false})} type="link"><LikeTwoTone style={{ fontSize: '20px' }}/></Button>
                                </Tooltip>
                              }
                            </> 
        },
      ]

      return(          

          <Table
                style={{marginTop:'20px'}}
                dataSource={enterprises.data}
                pagination={{
                    simple:true,                    
                    total: enterprises.quantity,
                    onChange: page => { enterprises.pagination(enterprises.dispatch,page) }
                }}
                footer={() => 'Datos proporcionados por API V1 - Smart Hydro'}
                loading={ enterprises.loading }
                columns={columns}
                rowKey='id' />          
      )
}

export default ListClients