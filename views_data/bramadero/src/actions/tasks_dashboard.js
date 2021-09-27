
import api from '../api/endpoints'

import React from 'react'

import { notification, Modal } from 'antd'
import { SmileOutlined, WarningOutlined, DeleteOutlined } from '@ant-design/icons';


export const getTotals = async(dispatch) =>{
    try{

        dispatch({type: 'DASHBOARD_LOADING'})

        const tasks = await api.tasks.get_total_tasks()
        
        dispatch({
            type: 'GET_TOTALS',
            payload: tasks
        })

    }catch(error){
        dispatch({
            type: 'ERROR',
            error:error
        })
    }
}

export const getTotalTasks= async(dispatch)=>{    
    
    dispatch({type: 'TABLE_LOADING', page: 1})
    
    try{
        dispatch({type: 'FALSE_ALL_FILTER'})
        
        const tasks = await api.tasks.get_tasks(1)
        
        dispatch({
            type: 'GET_DATA',
            payload: tasks,
            page: 1
        })

        }catch(error){
            
            dispatch({
                type: 'ERROR',
                payload: error
            })

        }

}

export const getActiveTasks = async(dispatch, state) =>{
    dispatch({type: 'TABLE_LOADING', page: state.page})
        try{
            dispatch({type: 'ACTIVE_FILTER'})
            const tasks = await api.tasks.get_tasks(1, {is_active:true})

            dispatch({
                type: 'GET_DATA',
                payload: tasks,
                page: 1
            })

        }catch(error){
            dispatch({
                type: 'ERROR',
                payload: error
            })
        }
}

export const getPriorityTasks = async(dispatch, state) =>{
    dispatch({type: 'TABLE_LOADING', page: state.page})

        try{
            dispatch({type: 'PRIORITY_FILTER'})
            const tasks = await api.tasks.get_tasks(1, {is_priority:true})
            dispatch({
                type: 'GET_DATA',
                payload: tasks,
                page: 1
            })

        }catch(error){
            dispatch({
                type: 'ERROR',
                payload: error
            })
        }
}

export const getCompleteTasks = async(dispatch, state) =>{
    dispatch({type: 'TABLE_LOADING', page: state.page})
        dispatch({type: 'COMPLETE_FILTER'})
        try{

            const tasks = await api.tasks.get_tasks(1, {is_complete:true})
            dispatch({
                type: 'GET_DATA',
                payload: tasks,
                page: 1
            })

        }catch(error){
            dispatch({
                type: 'ERROR',
                payload: error
            })
        }
}

export const getPagination = async(dispatch, state, page) =>{
    dispatch({
        type:'TABLE_LOADING', page: page
    })

    if(state.filters.is_active){
        const tasks = await api.tasks.get_tasks(page, {is_active:true})
        dispatch({
            type: 'PAGINATION',
            payload: tasks,
            page: page
        })
    } else
    if(state.filters.is_priority){
        const tasks = await api.tasks.get_tasks(page, {is_prirority:true})
        dispatch({
            type: 'PAGINATION',
            payload: tasks,
            page: page
        })
    } else
    if(state.filters.is_complete){
        const tasks = await api.tasks.get_tasks(page, {is_complete: true})
        dispatch({
            type: 'PAGINATION',
            payload: tasks,
            page: page
        })
    }else{
        const tasks = await api.tasks.get_tasks(page)
        dispatch({
            type: 'PAGINATION',
            payload: tasks,
            page: page
        })
    }
}

export const updateTasks = async(dispatch, state) =>{
    dispatch({
        type:'TABLE_LOADING',
        page: state.page
    })
    const totals = await api.tasks.get_total_tasks()
    
    dispatch({
        type: 'UPDATE_TOTALS',
        payload: totals
    }) 

    if(state.filters.is_active){
       const data = await api.tasks.get_tasks(state.page, {is_active: true})
       dispatch({
        type: 'GET_DATA',
        payload: data,
        page: state.page
    })

    }else if(state.filters.is_priority){

        const data = await api.tasks.get_tasks(state.page, {is_priority: true})
        dispatch({
            type: 'GET_DATA',
            payload: data,
            page: state.page
        })

    }else if(state.filters.is_complete){            
        const data = await api.tasks.get_tasks(state.page, {is_complete: true})
        dispatch({
            type: 'GET_DATA',
            payload: data,
            page: state.page
        })

    }else{            
        const data = await api.tasks.get_tasks(state.page)            
        dispatch({
            type: 'GET_DATA',
            payload: data,
            page: state.page
        })

    }
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
                    updateTasks(dispatch, state)        
                            
                }
        }         
    })
} 

export const finishTaskModal = (id_task, update) =>{
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
                    update()
                    Modal.destroyAll()
                }
        }         
    })
}

export const updateTask = async (dispatch, id_task, data, state) =>{
    
    const request = await api.tasks.update_task(id_task, data)    

    updateTasks(dispatch, state)

    return request
}

export const deleteTask = (dispatch, id_task, state) => {
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
                    updateTasks(dispatch, state)            
                }
        }         
    })

}