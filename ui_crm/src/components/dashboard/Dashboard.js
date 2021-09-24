//React
import React, { useEffect, useReducer } from 'react'

//Ant Design
import { Table, Spin, Button, Tag, Modal,
    Row, Col, Card, Statistic, Tooltip } from 'antd'

import { StopOutlined, AlertTwoTone, WarningTwoTone,
    CheckCircleTwoTone, AppstoreTwoTone, BookTwoTone,
    ReloadOutlined, FilterOutlined, SmileOutlined,
    WarningFilled, WarningOutlined, DeleteOutlined
 } from '@ant-design/icons'

//Reducer
import { reducer } from '../../reducers/dashboard'

//Actions
import { getTotalTasks, getActiveTasks, getPriorityTasks, 
    getCompleteTasks, getPagination, getTotals, updateTasks, 
    finishTask, updateTask,deleteTask } from '../../actions/tasks_dashboard'

import { viewTask } from '../../actions/tasks'
import { viewPerson } from '../../actions/employess'

//Components
import ModalEnterprise from '../../components/clients/ModalEnterprise'


const Dashboard = () =>{
    
    const initialState = {
        loading:false,
        filters:{
            is_active: false,
            is_priority: false,
            is_complete: false
        },        
        page: 1,
        loading_table:false,
        totals:{
            total:null,
            actives: null,
            priority: null,
            completes: null
        },
        quantity: null,
        data: null,
        error:null,
    }    

    const [state, dispatch] = useReducer(reducer, initialState)

    const totalTasks = () =>{     

        getTotalTasks(dispatch)
    }

    const activeTasks = () => {
        
        getActiveTasks(dispatch, state)
        
    }

    const priorityTasks = () =>{

        getPriorityTasks(dispatch, state)

    }

    const completesTasks = () =>{

        getCompleteTasks(dispatch, state)
        
    }

    const pagination = (page) =>{

        getPagination(dispatch, state, page)
        
    }

    useEffect(() => {

        getTotals(dispatch)
                
    }, [])

    const updateData = async () => {
        
        updateTasks(dispatch, state)
                
    }
    
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
            filteredValue: client => client.name || null,
            render: client => client ? <Button onClick={() => ModalEnterprise(client)} type='primary'>{client.name}</Button> : <StopOutlined />,                      
        },
        {
            title: 'Persona',
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
        { title: '', dataIndex: '', key: 'x', render: task => task.is_complete ?
                <>
                    <Button type="primary" style={{marginRight:'10px'}} onClick={() => viewTask(task)}>Ver</Button>
                    <Tooltip  title='Fecha que se completo la tarea'>
                    {task.date_complete && <Button disabled type="dashed" style={{borderColor:'#1890ff', color:'#1890ff'}} >{task.date_complete.slice(0,10)}</Button>}
                    
                    </Tooltip>
                    <SmileOutlined style={{ paddingLeft: '20px', fontSize:'24px', color:'#1890ff' }}/>
                </>
                :
                <>
                    <Button type="primary" style={{marginRight:'10px'}}  onClick={() => viewTask(task)} >Ver</Button>
                    <Button onClick ={ () => finishTask(dispatch,task.id, state) } type="dashed" style={{borderColor:'green', color:'green', marginRight:'20px'}}>Completar</Button>                    
                    
                    {task.is_priority ? 
                        <Tooltip title='Quitar de Prioridades'>
                            <Button onClick={() => updateTask(dispatch, task.id, {is_priority: false}, state)}  type="link">
                                <WarningFilled style={{fontSize:'20px', marginLeft:'45px', color: 'red'}}  />
                            </Button>                            
                        </Tooltip>
                    :
                    <>
                    <Tooltip  title='Eliminar tarea'>
                    <Button shape="link" onClick ={ () => deleteTask(dispatch, task.id, state)} type="danger" style={{marginRight:'10px'}} >
                        <DeleteOutlined style={{color:'red', fontSize:'20px'}} />
                    </Button>
                    </Tooltip>
                        <Tooltip title='Agregar a Prioridades'>
                            <Button onClick={() => updateTask(dispatch, task.id, {is_priority: true}, state)}  type="link">
                                <WarningOutlined style={{fontSize:'20px', marginLeft:'25px', color: 'red'}}  />
                            </Button>
                        </Tooltip>
                        </>
                    }
                    
                    
                </>
        },

      ]

    return(
        <React.Fragment>
        {
            state.loading === true ? <Spin size="large" style={{ marginLeft:'40%', marginTop:'15%'}} />:
            <>            
            <Tooltip title='Actilizar Datos'>
                <Button onClick={ updateData } shape="circle" type="primary" style={{marginBottom:'20px'}}><ReloadOutlined /></Button>
            </Tooltip>
            <Row gutter={16}>
                <Col span={24}>
                    <Card>
                        <Card.Grid style={{height:'100px', width:'25%'}}>
                            <Row>
                                <Col style={{marginRight:'20px'}}>
                                    <BookTwoTone style={{fontSize:'40px', marginLeft:'20%'}} />
                                </Col>
                                <Col >
                                    <Statistic title="TOTAL" value={state.totals.total} prefix={<AppstoreTwoTone />} />
                                </Col>
                                <Col>
                                    <Tooltip  title="Filtrar">
                                        <Button onClick={ () => {
                                            totalTasks()
                                        }} style={{ marginLeft:'40px', marginTop:'20px'}} type="primary" shape="circle" icon={<FilterOutlined />} />
                                    </Tooltip>
                                </Col>
                            </Row>
                        </Card.Grid >
                        <Card.Grid style={{height:'100px', width:'25%'}}>
                            <Row>
                                <Col style={{marginRight:'20px'}}>
                                    <AlertTwoTone style={{fontSize:'40px', marginLeft:'20%'}} />
                                </Col>
                                <Col >
                                    <Statistic title="ACTIVAS" value={state.totals.actives} prefix={<AppstoreTwoTone />} />
                                </Col>
                                <Col>
                                    <Tooltip  title="Filtrar">
                                        <Button onClick={ () => {
                                            activeTasks()
                                        }} style={{ marginLeft:'40px', marginTop:'20px'}} type="primary" shape="circle" icon={<FilterOutlined />} />
                                    </Tooltip>
                                </Col>
                            </Row>
                        </Card.Grid >
                        <Card.Grid style={{height:'100px', width:'25%'}} >
                            <Row>
                                <Col style={{marginRight:'20px'}}>
                                    <WarningTwoTone style={{fontSize:'40px', marginLeft:'20%'}} />
                                </Col>
                                <Col>
                                    <Statistic title="PRIORIDAD" value={state.totals.priority} prefix={<AppstoreTwoTone />} />
                                </Col>
                                <Col>
                                    <Tooltip  title="Filtrar">
                                        <Button onClick={() => { priorityTasks() }} style={{ marginLeft:'40px', marginTop:'20px'}} type="primary" shape="circle" icon={<FilterOutlined />} />
                                    </Tooltip>
                                </Col>
                            </Row>
                        </Card.Grid>
                        <Card.Grid style={{height:'100px', width:'25%'}} >
                            <Row>
                                <Col style={{marginRight:'10px'}}>
                                    <CheckCircleTwoTone style={{fontSize:'40px', marginLeft:'20%'}} />
                                </Col>
                                <Col>
                                    <Statistic title="COMPLETADAS" value={state.totals.completes} prefix={<AppstoreTwoTone />} />
                                </Col>
                                <Col>
                                    <Tooltip  title="Filtrar">
                                        <Button onClick={() => { completesTasks() }} style={{ marginLeft:'40px', marginTop:'20px'}} type="primary" shape="circle" icon={<FilterOutlined />} />
                                    </Tooltip>
                                </Col>
                            </Row>
                        </Card.Grid>
                    </Card>
                </Col>
            </Row>
            <div style={{margin:'20px'}}>                
                {state.filters.is_active && <Tag closable onClose={() => totalTasks()} color="processing">ACTIVAS</Tag>}
                {state.filters.is_priority && <Tag closable onClose={() => totalTasks()} color="volcano">PRIORIDAD</Tag>}
                {state.filters.is_complete && <Tag closable onClose={() => totalTasks()} color="geekblue">COMPLETADAS</Tag>}
                {!state.filters.is_active & !state.filters.is_priority & !state.filters.is_complete ? <Tag color="magenta">Sin Filtros</Tag> :''}
            </div>
            <Table
                style={{marginTop:'20px'}}
                dataSource={state.data}
                pagination={{
                    simple:true,
                    current: state.page,
                    total: state.quantity,
                    onChange: page => { pagination(page) }
                }}
                footer={() => 'Datos proporcionados por API V1 - Smart Hydro'}
                loading={state.loading_table}
                columns={columns}
                rowKey='id' />
            </>
        }
        </React.Fragment>
        )
}

export default Dashboard