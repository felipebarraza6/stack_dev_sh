
import api from '../api/endpoints'

import React from 'react'

import moment from 'moment'

import { Modal, notification, Descriptions, Tag, Form, Input, Button, DatePicker} from 'antd'

import { DeleteOutlined, WarningOutlined, SmileOutlined,
        CheckCircleFilled, BookFilled, CheckCircleTwoTone, 
        MinusCircleTwoTone, ApiTwoTone } from '@ant-design/icons'

const { TextArea } = Input

export const reloadTasks = async(
        dispatch, 
        pages= {totals:1, actives: 1, priorities: 1, completes: 1},
        date_range={start_date:'', end_date:''},
        year='',
        month='',
        day='',
        id_person='',
        id_enterprise=''
        ) =>{

    try{
        const totals = await api.tasks.get_tasks(
            pages.totals,
            '',
            {
                start_date:date_range.start_date, 
                end_date:date_range.end_date
            },
            year, month, day, 
            id_person, id_enterprise
        )

        const actives = await api.tasks.get_tasks(
            pages.actives, 
            {is_active:true}, 
            {
                start_date:date_range.start_date, 
                end_date:date_range.end_date
            },
            year, month, day, 
            id_person, id_enterprise
        )

        const priorities = await api.tasks.get_tasks(
            pages.priorities, 
            {is_priority:true}, 
            {
                start_date:date_range.start_date, 
                end_date:date_range.end_date
            }, 
            year, month, day, 
            id_person, id_enterprise
        )

        const completes = await api.tasks.get_tasks(
            pages.completes, 
            {is_complete:true}, 
            {
                start_date:date_range.start_date, 
                end_date:date_range.end_date
            }, 
            year, month, day, 
            id_person, id_enterprise
        )

        dispatch({type:'CLEAN_RANGE_DATE'})

        dispatch({
            type:'RELOAD_ALL_DATA',
            payload: {
                totals:totals,
                actives:actives,
                priority:priorities,
                completes:completes,
                date_range:date_range,
                year:year,
                month:month,
                day:day,
                id_enterprise_selected:id_enterprise,
                id_person_selected:id_person

            }
        })

    }catch(error){
        console.log({error})
    }
    
}

export const updateTaskModal = async(dispatch, task, state) => {

    if(task){
        task = {
            ...task,
            'date':moment(task.date)
        }
    }

    const onFinish = async(value) => {
        
        if(value.date){
            value = {
                ...value,
                'date':moment(value.date).format('YYYY-MM-DDTHH:mm:ss')
            }
        }
        
        const update_task = await api.tasks.update_task(task.id, value)
        
            if(update_task.status){
                notification.open({
                    message: `Tarea Actualizada!`,
                    description: `La tarea "${task.id}" fue actualizada`,
                    icon: <BookFilled />
                })
                reloadTasks(
                    dispatch, 
                    {
                        totals:state.pageTotals, 
                        actives:state.pageActives, 
                        priorities:state.pagePriority, 
                        completes:state.pageCompletes
                    }, 
                    {
                        start_date:state.date_range.start_date, 
                        end_date:state.date_range.end_date
                    }, 
                    state.year, state.month, state.day,
                    state.id_person_selected,
                    state.id_enterprise_selected
                )      
                Modal.destroyAll()                    
            }                
    }

    try{

        Modal.info({
            title: `Actualizar la tarea "${task.id}"`,
            width: '400px',
            maskClosable: true,
            content: <> 
            <Form
                    layout="vertical"
                    name="update_types"
                    style={{marginTop:'20px'}}
                    onFinish = {onFinish}
                    initialValues={task}                    
                >

                    <Form.Item
                        style={{width:'100%', marginBottom:'10px'}}
                        name="note"
                        label="Nota"
                        rules={[
                            {
                              required: true,
                              message: 'Escribe una Nota',
                            },
                          ]}                        
                    >
                        <TextArea placeholder="Nota..."/>
                    </Form.Item>

                    <Form.Item name="date" label="Fecha de ejecución" rules={[{required: true,message: 'Selecciona una fecha',}]}>
                        <DatePicker style={{width:'100%'}} showTime={{ format: 'HH:mm:ss' }} />
                    </Form.Item>

                     <Button type="primary" style={{marginRight:'5px'}} htmlType="submit" >Actualizar</Button>
                     <Button type="danger" onClick={() =>{Modal.destroyAll()} } >Cancelar</Button>                                       
                </Form>
            </>,
            okButtonProps:{ style: { display: 'none' } },
            
        })
        

    }catch(error){
        console.log(error)
    }
}


export const paginationTotals = async(dispatch, page, state)=>{
    console.log(state)
    try{

        dispatch({ type: 'LOADING_TOTALS' })
        const tasks_totals = await api.tasks.get_tasks(
            page, 
            '', 
            {
                start_date:state.date_range.start_date, 
                end_date:state.date_range.end_date
            }, 
            state.year, state.month, state.day,
            state.id_person_selected,
            state.id_enterprise_selected
        )

        dispatch({
            type:'PAGINATION_TOTALS',
            payload: tasks_totals,
            page: page
        })

    }catch(error){
        console.log({error})
    }
}

export const paginationActives = async(dispatch, page, state) =>{
    try {
        dispatch({type: 'LOADING_ACTIVES'})
        const tasks_actives = await api.tasks.get_tasks(
            page, 
            {is_active:true}, 
            {
                start_date:state.date_range.start_date, 
                end_date:state.date_range.end_date
            }, 
            state.year, state.month, state.day,
            state.id_person_selected,
            state.id_enterprise_selected
            
        )

        dispatch({
            type:'PAGINATION_ACTIVES',
            payload: tasks_actives,
            page: page
        })
    }catch(error){
        console.log(error)
    }
}

export const paginationPriorities = async(dispatch, page, state) =>{
    try{
        dispatch({type:'LOADING_PRIORITIES'})
        const tasks_priorities = await api.tasks.get_tasks(
            page, 
            {is_priority:true}, 
            {
                start_date:state.date_range.start_date, 
                end_date:state.date_range.end_date
            }, 
            state.year, state.month, state.day,
            state.id_person_selected,
            state.id_enterprise_selected    
        )

        dispatch({
            type:'PAGINATION_PRIORITIES',
            payload: tasks_priorities,
            page: page
        })
    }catch(error){
        const tasks_priorities = await api.tasks.get_tasks(1, {is_priority:true}, {start_date:state.date_range.start_date, end_date:state.date_range.end_date}, state.year, state.month, state.day)
        dispatch({
            type:'PAGINATION_PRIORITIES',
            payload: tasks_priorities,
            page: 1
        })
    }
}

export const paginationCompletes = async(dispatch, page, state)=>{
    try{
        dispatch({type:'LOADING_COMPLETES'})
        const tasks_completes = await api.tasks.get_tasks(
            page, 
            {is_complete:true}, 
            {
                start_date:state.date_range.start_date, 
                end_date:state.date_range.end_date
            }, 
            state.year, state.month, state.day,
            state.id_person_selected,
            state.id_enterprise_selected
        )

        dispatch({
            type:'PAGINATION_COMPLETES',
            payload: tasks_completes,
            page: page
        })
    }catch(error){
        console.log(error)
    }
}

export const deleteTask = (id_task, state, dispatch) => {
    Modal.confirm({
        title:`Eliminar tarea #${id_task}`,
        icon: <DeleteOutlined style={{ color: 'red'}}/>,
        content: `Estas seguro de liminar la tarea #${id_task}, una vez eliminada no podrás recuperar este registro`,
        okText: 'ELIMINAR',
        okType: 'danger',
        cancelType: 'danger',
        width: '600px',
        onOk: async() =>{
                const data = await api.tasks.delete_task(id_task)
                if(data.status){
                    notification.open({
                        message: `Tarea Eliminada!`,
                        description: `La tarea #${id_task} fue eliminada`,
                        icon: <DeleteOutlined style={{ color: '#red'}} />
                    })                    
                }
                reloadTasks(dispatch, {totals:state.pageTotals, actives:state.pageActives, priorities:state.pagePriority, completes:state.pageCompletes}, {start_date:state.date_range.start_date, end_date:state.date_range.end_date}, state.year, state.month, state.day)
        }         
    })

}

export const finishTask = (dispatch, id_task, state) =>{
    
    Modal.confirm({
        title:'Precaución',
        icon: <WarningOutlined/>,
        content: `Estas seguro de querer completar la tarea #${id_task}, una vez completada una tarea no podrás re abrirla, editarla o eliminarla.`,
        okText: 'COMPLETAR',
        width: '600px',
        onOk: async() =>{
                const data = await api.tasks.finish_task(id_task)
                if(data.status){
                    notification.open({
                        message: `Tarea Completada!`,
                        description: `La tarea #${id_task} fue completada`,
                        icon: <SmileOutlined style={{ color: '#108ee9'}} />
                    })
                    reloadTasks(dispatch, {totals:state.pageTotals, actives:state.pageActives, priorities:state.pagePriority, completes:state.pageCompletes}, {start_date:state.date_range.start_date, end_date:state.date_range.end_date}, state.year, state.month, state.day)            
                }
        }         
    })
} 

export const updateTaks = async(id_task, dispatch, state, data) =>{
    try{
        const task = await api.tasks.update_task(id_task, data)
        if(task.status){
            notification.open({
                message: 'Tarea Actualizada!',
                description: `La tarea #${id_task} fue actualizada`,
                icon: <CheckCircleFilled />
            })
        }
        reloadTasks(
            dispatch, 
            {
                totals:state.pageTotals, 
                actives:state.pageActives, 
                priorities:state.pagePriority, 
                completes:state.pageCompletes
            }, 
            {
                start_date:state.date_range.start_date, 
                end_date:state.date_range.end_date
            }, 
            state.year, state.month, state.day,
            state.id_person_selected,
            state.id_enterprise_selected
        )

    }catch(error){
        console.log(error)
    }
}

export const viewTask = (task) => {
    Modal.info({
        title:<>
            {task.type_action} | {task.employee.name}({task.employee.enterprise})
            </>,
        icon: <BookFilled style={{ color: '#1890ff'}}/>,
        content: <>
            <Descriptions title={`Tarea #${task.id} - ${task.user}`} layout="vertical" bordered>
                <Descriptions.Item label="Tipo de tarea">
                    {task.type_action}
                </Descriptions.Item>
                
                <Descriptions.Item label="Fecha de creación" >
                    <Tag color="blue">{task.created.slice(0,10)}</Tag> 
                    <Tag color="blue">{task.created.slice(11,19)} hrs</Tag>
                </Descriptions.Item>

                <Descriptions.Item label="Fecha de ejecución" >
                <Tag color="magenta">{task.date.slice(0,10)}</Tag> 
                    <Tag color="magenta">{task.date.slice(11,19)} hrs</Tag>
                </Descriptions.Item>

                <Descriptions.Item label="Nota" span={3}>                    
                    {task.note}
                </Descriptions.Item>

                <Descriptions.Item style={{textAlign:'center'}} label="ACTIVA">
                    {task.is_active ? <CheckCircleTwoTone twoToneColor="#87d068" style={{fontSize:'20px'}}/> : <MinusCircleTwoTone twoToneColor="red" style={{fontSize:'20px'}}/>}
                </Descriptions.Item>

                <Descriptions.Item style={{textAlign:'center'}} label="PRIORIDAD">
                    {task.is_priority ? <CheckCircleTwoTone twoToneColor="#87d068" style={{fontSize:'20px'}}/> : <MinusCircleTwoTone twoToneColor="red" style={{fontSize:'20px'}}/>}
                </Descriptions.Item>

                <Descriptions.Item style={{textAlign:'center'}} label="COMLPETADA">
                    {task.is_complete ? <CheckCircleTwoTone twoToneColor="#87d068" style={{fontSize:'20px'}}/> : <MinusCircleTwoTone twoToneColor="red" style={{fontSize:'20px'}}/>}
                </Descriptions.Item>
            </Descriptions>
            
            <Descriptions title={`${task.employee.name}`} bordered style={{marginTop:'20px'}}>
                <Descriptions.Item label="Empresa" span={3}>
                    {task.employee.enterprise}
                </Descriptions.Item>
            
                <Descriptions.Item label="Cargo" span={3}>
                    {task.employee.charge}
                </Descriptions.Item>
            
                <Descriptions.Item label="Email" span={3}>
                    {task.employee.email}
                </Descriptions.Item>
            
                <Descriptions.Item label="Telefono" span={3}>
                    {task.employee.phone_number}
                </Descriptions.Item>
            </Descriptions>
        </>,
        okText: 'OK',
        width: '900px'      
    })

}

export const getTypeTasks = async(dispatch, page) =>{
    try{
        dispatch({type:'LOADING_TYPES'})

        const type_tasks = await api.type_tasks.get_type_actions(page)

        dispatch({
            type: 'GET_TYPE_TASKS',
            payload: type_tasks,
            page:page
        })

    }catch(error){
        console.log({error})
    }
}

export const postTypeTasks = async(dispatch, data) =>{
    
    try{                

        const type_task = await api.type_tasks.create_type_task(data)
        if(type_task.status){
            getTypeTasks(dispatch, 1)
        }                

    }catch(error){
        console.log({error})
    }
}

export const deleteTypeTask = async(dispatch, id_type, state) =>{
    console.log(state)
    Modal.confirm({
        title:`Eliminar tipo de tarea "${id_type.description}"`,
        icon: <DeleteOutlined style={{ color: 'red'}}/>,
        content: `Estas seguro de eliminar el tipo de tarea #${id_type.id}, una vez eliminada no podrás recuperar este registro`,
        okText: 'ELIMINAR',
        okType: 'danger',
        cancelType: 'danger',
        width: '600px',
        onOk: async() =>{                
                const data = await api.type_tasks.delete_type_task(id_type.id)
                if(data.status){
                    notification.open({
                        message: `Tipo de tarea Eliminada!`,
                        description: `El tipo de tarea ${id_type.description} fue eliminada`,
                        icon: <DeleteOutlined style={{ color: '#red'}} />
                    })                    
                }
                getTypeTasks(dispatch,state.page )
        }    
    })
}

export const updateTypeTask = async(dispatch, type_task, state) => {

    const onFinish = async(value) => {
        
        const update_task = await api.type_tasks.update_type_task(value.id, value)
        
            if(update_task.status){
                notification.open({
                    message: `Tipo de tarea Actualizada!`,
                    description: `El tipo de tarea "${value.description}" fue actualizada`,
                    icon: <ApiTwoTone style={{ color: '#red'}} />
                })
                getTypeTasks(dispatch,state.page)            
                Modal.destroyAll()                    
            }                
    }

    try{

        Modal.info({
            title: `Actualizar "${type_task.description}"`,
            width: '700px',
            maskClosable: true,
            content: <> 
            <Form
                    layout="inline"
                    name="update_types"
                    style={{marginTop:'20px'}}
                    onFinish = {onFinish}
                    initialValues={type_task}                    
                >
                    <Form.Item
                        style={{width:'60%', marginBottom:'10px'}}
                        name="id"                     
                    >   
                        <Input hidden={true} />
                    </Form.Item>

                    <Form.Item
                        style={{width:'60%', marginBottom:'10px'}}
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

                     <Button type="primary" style={{marginRight:'5px'}} htmlType="submit" >Actualizar</Button>
                     <Button type="danger" onClick={() =>{Modal.destroyAll()} } >Cancelar</Button>                                       
                </Form>
            </>,
            okButtonProps:{ style: { display: 'none' } },
            
        })
        

    }catch(error){
        console.log(error)
    }
}
