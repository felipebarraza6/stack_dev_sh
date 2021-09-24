//React
import React from 'react'

//Antd
import { Table, Typography, Button, Dropdown, Menu } from 'antd'
import { EyeOutlined, EditOutlined, DeleteOutlined,
        WarningFilled, WarningOutlined, CheckCircleOutlined, 
        MenuOutlined } from '@ant-design/icons'

//Actions
import { deleteTask, finishTask, updateTaks, viewTask, updateTaskModal } from '../../actions/tasks'

const { Text } = Typography;

const TableTasks = ({ dispatch, data, title, icon, count, loading, pagination, state }) =>{
    
    const columns = [
        {
            title: 'Tarea',
            dataIndex: 'type_action'
        },
        {
            title: 'Persona',
            dataIndex: 'employee',
            render: (person) => person ? person.name : ''
        },
        {
            title: 'Empresa',
            dataIndex: 'employee',
            render: (person) => person ? person.enterprise : ''
        },
        {
            render: (person) => <React.Fragment>
                                    <Dropdown 
                                        overlay={ 
                                            <Menu >
                                                <Menu.Item key="2">
                                                    <Button type="link" style={{color:'#1890ff'}} onClick={()=>{viewTask(person)}}>
                                                        <EyeOutlined/> Ver Tarea
                                                    </Button>
                                                </Menu.Item>

                                                {!person.is_complete & !person.is_priority &&
                                                <Menu.Item key="1">
                                                    <Button type="link" style={{color:'grey'}} onClick={() =>{updateTaskModal(dispatch, person, state)}}>
                                                        <EditOutlined/> Editar
                                                    </Button>
                                                </Menu.Item>
                                                }

                                                {!person.is_priority & !person.is_complete &&
                                                <Menu.Item key="3">
                                                    <Button type="link" style={{color:'orange'}} onClick={() =>{updateTaks(person.id, dispatch, state, {is_priority:true})}}>
                                                        <WarningFilled/> Agregar a prioridades
                                                    </Button>
                                                </Menu.Item>
                                                }

                                                {person.is_priority &&
                                                <Menu.Item key="4">
                                                    <Button type="link" style={{color:'grey'}} onClick={() =>{updateTaks(person.id, dispatch, state, {is_priority:false})}}>
                                                    <WarningOutlined/> Quitar de prioridades
                                                </Button>
                                            </Menu.Item>
                                                }

                                                {!person.is_complete &&
                                                    <Menu.Item key="5">
                                                    <Button type="link" style={{color:'green'}} onClick={() => { finishTask(dispatch, person.id, state)}} >
                                                        <CheckCircleOutlined/> Completar
                                                    </Button>
                                                </Menu.Item>
                                                }
                                                
                                                {!person.is_priority & !person.is_complete &&
                                                <Menu.Item key="6">
                                                    <Button style={{color:"red"}} type="link" onClick={() => { deleteTask(person.id, state, dispatch) }}>
                                                        <DeleteOutlined/> Eliminar
                                                    </Button>
                                                </Menu.Item>
                                                }
                                            </Menu>}
                                    >
                                        <Button type="link">
                                            <MenuOutlined style={{fontSize:'16px'}} />
                                        </Button>
                                    </Dropdown>
                                </React.Fragment>
        }
    ]

    return (
        <Table 
            
            loading={loading}
            style={{margin:'2px'}}
            title={() => <><Text strong>{title}</Text> ({count}) {icon}</>}
            columns={columns}
            dataSource={data}
            rowKey='id'
            pagination={{
                simple:true,
                total: count,
                onChange: (page) => pagination(dispatch, page, state)
            }}
        />
    )

}

export default TableTasks



