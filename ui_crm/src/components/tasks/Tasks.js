//React
import React, { useReducer, useEffect } from 'react'

//Antd
import { Spin, Row, Col, Button, Tooltip, Alert } from 'antd'
import { BookFilled, AlertFilled, WarningFilled, CheckCircleFilled,
    SyncOutlined } from '@ant-design/icons'

//Components
import Totals from './Totals'
import TableTasks from './TableTasks'
import FormTask from './FormTask'
import FormTypeTasks from './FormTypeTasks'
import FilterDateTasks from './FilterDateTasks'
import FilterEnterprise from './FilterEnterprise'
import FilterPerson from './FilterPerson'

//Reducers
import { reducer } from '../../reducers/tasks'

//Actions
import { paginationTotals, paginationActives, paginationPriorities, paginationCompletes, reloadTasks } from '../../actions/tasks'


const Tasks = () =>{
    
    const initialState ={

        totals: null,
        loading: false,
        
        totalsData: null,
        activesData: null,
        priorityData: null,
        completesData: null,

        pageTotals: 1,
        pageActives: 1,
        pagePriority: 1,
        pageCompletes: 1,

        loadingTotals: false,
        loadingActives: false,
        loadingPriority: false,
        loadingCompletes: false,

        countTotals: 0,
        countActives: 0,
        countPriority: 0,
        countCompletes: 0,
        
        date_range:{
            start_date:'',
            end_date:''
        },

        year:'',
        month:'',
        day:'',
            
        filter_enterperises:null,
        filter_persons:null,
        id_enterprise_selected:'',
        id_person_selected:''
        
    }

    const [state, dispatch] = useReducer(reducer, initialState)

    useEffect(() => {
        dispatch({type:'LOADING'})
        reloadTasks(dispatch, {totals:1, actives:1, priorities:1, completes:1})
    }, [])

    return(
        <React.Fragment>
            
            {state.loading ? <Spin size="large" style={{ marginLeft:'40%', marginTop:'15%'}} />:
            <>
            
            <Totals totals={state.totals} dispatch={dispatch} />
            

            <Row style={{marginTop:'20px'}}>
                <Col span={7} style={{marginRight:'10px'}}>

                     <FilterDateTasks dispatch={dispatch} state={state} />

                </Col>
                <Col span={6} style={{marginRight:'10px'}}>
                    
                    <FilterEnterprise dispatch={dispatch} state={state} />
                     
                </Col>
                <Col span={6} style={{marginRight:'10px'}}>

                    <FilterPerson dispatch={dispatch} state={state} />         

                </Col>
                <Col span={3} style={{marginLeft:'80px'}}>                     
                <Tooltip  title="Actualizar">
                        <Button type="link" shape="circle"
                            onClick={()=>{
                                dispatch({type:'LOADING_TABLES'})
                                dispatch({type:'CLEAN_RANGE_DATE'})
                                reloadTasks(dispatch, {totals:1, actives:1, priorities:1, completes:1})

                            }}
                            style={{marginRight:'20px'}}
                        >
                            <SyncOutlined style={{fontSize:'30px'}} />
                        </Button>
                    </Tooltip>
                   
                    
                    <FormTask dispatch={dispatch} />                                        
                    <FormTypeTasks />
                    
                </Col>
            </Row>

            <Row style={{marginBottom:'',marginTop:'15px'}}>
                {state.date_range.start_date && <>
                    <Alert 
                        message={`Datos filtranos desde ${state.date_range.start_date} a ${state.date_range.end_date}`} 
                        type="success"
                        onClose={() => {
                            dispatch({type:'CLEAN_RANGE_DATE'})
                            dispatch({type:'LOADING_TABLES'})
                            reloadTasks(dispatch, {totals:1, actives:1, priorities:1, completes:1})
                            }
                        } 
                        showIcon 
                        closable />
                </>}
                {state.year && <>
                    <Alert 
                        message={`FILTRO: ${state.year} / ${state.month} / ${state.day} `} 
                        type="success"
                        onClose={() => {
                            dispatch({type:'CLEAN_RANGE_DATE'})
                            dispatch({type:'LOADING_TABLES'})
                            reloadTasks(dispatch, {totals:1, actives:1, priorities:1, completes:1})
                            }
                        } 
                        showIcon 
                        closable />
                </>}
                

            </Row>

            <Row style={{marginTop:'20px'}}>
                <Col span={6}>
                    <TableTasks 
                        dispatch={dispatch}
                        title={'Tareas totales'} 
                        data={state.totalsData} 
                        icon={<BookFilled style={{color:'#1890ff', float:'right', fontSize:'25px'}} />} 
                        count = {state.countTotals}
                        loading={state.loadingTotals}
                        pagination={paginationTotals}
                        state={state}
                    />
                </Col>
                <Col span={6}>
                    <TableTasks
                        dispatch={dispatch} 
                        title={'Tareas activas'} 
                        data={state.activesData}
                        icon={<AlertFilled style={{color:'orange', float:'right', fontSize:'25px'}} />}
                        count = {state.countActives}
                        loading={state.loadingActives}
                        pagination={paginationActives}
                        state={state}
                    />
                </Col>
                <Col span={6}>
                    <TableTasks 
                        dispatch={dispatch}
                        title={'Tareas prioritarias'} 
                        data={state.priorityData}
                        icon={<WarningFilled style={{color:'red', float:'right', fontSize:'25px'}} />} 
                        count = {state.countPriority}
                        loading={state.loadingPriority}
                        pagination={paginationPriorities}
                        state={state}
                    />
                </Col>
                <Col span={6}>
                    <TableTasks 
                        dispatch={dispatch}
                        title={'Tareas completadas'} 
                        data={state.completesData}
                        icon={<CheckCircleFilled style={{color:'green', float:'right', fontSize:'25px'}} />} 
                        count = {state.countCompletes}
                        loading={state.loadingCompletes}
                        pagination={paginationCompletes}
                        state={state}
                    />
                </Col>
            </Row>
            </>

            }
        </React.Fragment>
    )
}

export default Tasks