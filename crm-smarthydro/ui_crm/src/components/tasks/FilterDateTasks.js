import React, { useState } from 'react'

import { DatePicker, Card, Button, Switch, Tooltip, Typography, Collapse, Form } from 'antd'
import { FilterOutlined, CalendarTwoTone } from '@ant-design/icons'

import moment from 'moment'

import {reloadTasks} from '../../actions/tasks'

const { RangePicker } = DatePicker
const { Text } = Typography
const { Panel } = Collapse

const FilterDateTasks = (attr) =>{

    const [state, setState] = useState({

        range_date:true,
        range_year:false,
        range_month:false,

        only_date:false,
        only_year:false,
        year_mounth:false
    })


    return(
        <Collapse>
        <Panel header={<>FECHAS<CalendarTwoTone style={{float: 'right'}} /></>}>
                <Card
                bordered={false}
                title={
                    <>
            <Switch
                checked={state.range_date} 
                onChange={
                    (value)=> setState({range_date:true})
                    } 
                size="small" 
                style={{marginRight:'3px'}} /> 
                    <Text type="secondary">
                        Rangos
                    </Text>

            <Switch
                checked={state.only_date}
                onChange={(value)=> setState({only_date:true})} 
                size="small" 
                style={{marginRight:'3px', marginLeft: '10px'}} /> 
                    <Text type="secondary">Día</Text>

            <Switch
                checked={state.only_year}
                onChange={(value)=> setState({only_year:true})} 
                size="small" 
                style={{marginRight:'3px', marginLeft: '10px'}} /> 
                    <Text type="secondary">Año</Text>

            <Switch
                checked={state.year_mounth}
                onChange={(value)=> setState({year_mounth:true})} 
                size="small" 
                style={{marginRight:'3px', marginLeft: '10px'}} /> 
                    <Text type="secondary">Año y mes</Text>
            </>
                }
                >

               
            
            {state.range_date && <>
            <Form
                name="range"
                onFinish = {(values) => {
                    values = {
                        ...values,
                        'range_date':{
                            0: moment(values.range_date[0]).format('YYYY-MM-DD'),
                            1: moment(values.range_date[1]).format('YYYY-MM-DD')
                        }
                    }

                    reloadTasks(
                            attr.dispatch, 
                            {
                                totals:1, 
                                actives:1, 
                                priorities:1, 
                                completes:1
                            }, 
                            {
                                start_date:values.range_date[0], 
                                end_date:values.range_date[1]
                            }
                        ) 
                }}
                layout="inline"

            >
                <Form.Item name="range_date" style={{width:'80%'}} rules={[{ required: true, message: 'Ingresa en rango de fechas para utilizar el filtro'}]}>
                    <RangePicker style={{width:'100%'}} />
                </Form.Item>
                
                <Tooltip title="Filtrar">
                    <Button htmlType="submit" type="primary" shape="circle" style={{marginLeft:'20px'}}>
                        <FilterOutlined style={{fontSize:'15px'}} />
                    </Button>
                </Tooltip>
                
            </Form>
            </>}
            {state.only_date && <>
            <Form
                name="date"
                onFinish = {(values) => {
                    values = {
                        ...values,
                        'year':moment(values.date).format('YYYY'),
                        'month':moment(values.date).format('MM'),
                        'day':moment(values.date).format('DD')
                        }

                        reloadTasks(
                            attr.dispatch, 
                            {
                                totals:1, 
                                actives:1, 
                                priorities:1, 
                                completes:1
                            }, 
                            {},
                            values.year,
                            values.month,
                            values.day
                        )
                    }
                    
                }
                layout="inline"
            >   
            <Form.Item name="date" style={{width:'80%'}} rules={[{ required: true, message: 'Ingresa la fecha'}]}>
                <DatePicker style={{width:'100%'}} />
            </Form.Item>                
                <Tooltip title="Filtrar">
                    <Button htmlType="submit" type="primary" shape="circle" style={{marginLeft:'20px'}}>
                        <FilterOutlined style={{fontSize:'15px'}} />
                    </Button>
                </Tooltip>
            </Form>
            </>}
            {state.only_year && <>
                <Form
                name="date"
                onFinish = {(values) => {
                    values = {
                        ...values,
                        'year':moment(values.year).format('YYYY')
                        }
                        reloadTasks(
                            attr.dispatch, 
                            {
                                totals:1, 
                                actives:1, 
                                priorities:1, 
                                completes:1
                            }, 
                            {},
                            values.year
                        )
                    }
                    
                }
                layout="inline"
            >   
            <Form.Item name="year" style={{width:'80%'}} rules={[{ required: true, message: 'Ingresa la fecha'}]}>
                <DatePicker picker={'year'} style={{width:'100%'}} />
            </Form.Item>                
                <Tooltip title="Filtrar">
                    <Button htmlType="submit" type="primary" shape="circle" style={{marginLeft:'20px'}}>
                        <FilterOutlined style={{fontSize:'15px'}} />
                    </Button>
                </Tooltip>
            </Form>
            </>}
            {state.year_mounth && <>
                <Form
                name="date"
                onFinish = {(values) => {
                    values = {
                        ...values,
                        'year':moment(values.year_month).format('YYYY'),
                        'month':moment(values.year_month).format('MM')
                        }

                        reloadTasks(
                            attr.dispatch, 
                            {
                                totals:1, 
                                actives:1, 
                                priorities:1, 
                                completes:1
                            }, 
                            {},
                            values.year,
                            values.month
                        )
                    }
                    
                }
                layout="inline"
            >   
            <Form.Item name="year_month" style={{width:'80%'}} rules={[{ required: true, message: 'Ingresa la fecha'}]}>
                <DatePicker picker="month" style={{width:'100%'}} />
            </Form.Item>
                <Tooltip title="Filtrar">
                    <Button htmlType="submit" type="primary" shape="circle" style={{marginLeft:'20px'}}>
                        <FilterOutlined style={{fontSize:'15px'}} />
                    </Button>
                </Tooltip>
            </Form>
            </>}
            </Card>
            </Panel>        
                        
            </Collapse>
        
    )
    
}

export default FilterDateTasks