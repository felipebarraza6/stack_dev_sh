import React, { useContext, useState } from 'react'
import { Tag, Card, InputNumber as Input, Input as InputNormal,
        Col, Row, Badge,
        Select, Button, notification, Popconfirm } from 'antd'
import { QuotationContext } from '../../../containers/Quotation'
import { InternalLiftingContext } from '../../pages/InternalLifting'
import { ArrowRightOutlined, FileImageFilled } from '@ant-design/icons'

const { Option } = Select

const { TextArea } = InputNormal

const ListFormDataWell = () => {

    const { state, dispatch } = useContext(InternalLiftingContext)
    const  [isFlow, setIsFlow] = useState(false)


    const activeImg = (a) => {
        const granted_flow = state.wells.temporary_well.well_data.granted_flow.value
        const well_depth= state.wells.temporary_well.well_data.well_depth.value
        const static_level= state.wells.temporary_well.well_data.static_level.value
        const dynamic_level=state.wells.temporary_well.well_data.dynamic_level.value
        const pump_installation_depth=state.wells.temporary_well.well_data.pump_installation_depth.value
        const inside_diameter_well=state.wells.temporary_well.well_data.inside_diameter_well.value
        const duct_outside_diameter=state.wells.temporary_well.well_data.duct_outside_diameter.value
        const has_flow_sensor=state.wells.temporary_well.well_data.has_flow_sensor.value

        if(granted_flow<1){
            notification.error({description:'El caudal otorgado debe ser mayor a 1.0'})
        }
        else if(well_depth<1){
            notification.error({description:'La profundidad del pozo debe ser mayor a 1.0'})
        }
        else if(static_level<1){
            notification.error({description:'El nivel estático debe ser mayor a 1.0'})
        }
        else if(dynamic_level<1){
            notification.error({description:'El nivel dinámico debe ser mayor a 1.0'})
        }
        else if(pump_installation_depth<1){
            notification.error({description:'La profundidad de instalación de la bomba debe ser mayor a 1.0'})
        }
        else if(inside_diameter_well<1){
            notification.error({description:'El diámetro interior del pozo debe ser mayor a 1.0'})
        }
        else if(duct_outside_diameter<1){
            notification.error({description:'El diámetro exterior del ducto de salida debe ser mayor a 1.0'})
        } 
        else if(!has_flow_sensor){
            notification.error({description:'Debes seleccion una opción para "¿Cuanta con sensor de flujo?'})
        } else {

            dispatch({
                type:'SET_CURRENT',
                step:2
            })

            dispatch({
                type: 'SET_STEP_03',
                active: a ? true:false,
                finish: a ? true:false,
                hide: true,
                is_load_image: a ? true:false            
            })

            if(!state.wells.temporary_well.is_edit){                
                if(!a){
                    dispatch({
                        type: 'ADD_WELL_CONFIRM',
                        well: state.wells.temporary_well
                    }) 
                } 
                
            } else {                
                if(!a){
                    dispatch({
                        type: 'UPDATE_WELL',
                        well: state.wells.temporary_well
                    }) 
                }
                
                
            }
        }        
    }

    const data = [
        {
            title: 'Caudal otorgado',
            color: 'blue',
            name:'granted_flow',
            suffix: 'Lt/SEG',
            value: state.wells.temporary_well.well_data.granted_flow.value                    
        },
        {
            title: 'Profundidad total del pozo',
            color: 'blue',
            name:'well_depth',
            suffix: 'Mt',
            value: state.wells.temporary_well.well_data.well_depth.value          
        },
        {
            title: 'Nivel estático',
            color: 'blue',
            name:'static_level',
            suffix: 'Mt',
            value: state.wells.temporary_well.well_data.static_level.value
        },
        {
            title: 'Nivel dinámico',
            color: 'blue',
            name:'dynamic_level',
            suffix: 'Mt',
            value: state.wells.temporary_well.well_data.dynamic_level.value
        },
        {
            title: 'Profundidad instalación bomba',
            color: 'blue',
            name:'pump_installation_depth',
            suffix: 'Mt',
            value: state.wells.temporary_well.well_data.pump_installation_depth.value
        },
        {
            title: 'Diámetro interior pozo',
            color: 'blue',
            name:'inside_diameter_well',
            suffix: 'MM/PULG',
            value: state.wells.temporary_well.well_data.inside_diameter_well.value
        },
        {
            title: 'Diámetro exterior ducto salida bomba',
            color: 'blue',
            name:'duct_outside_diameter',
            suffix: 'MM/PULG',
            value: state.wells.temporary_well.well_data.duct_outside_diameter.value
        },
        {
            title: '¿Cuenta con sensor de flujo?',
            color: 'geekblue',
            name:'has_flow_sensor',
            suffix: 'SI/NO',
            value: state.wells.temporary_well.well_data.has_flow_sensor.value
        },
        {
            title: '¿Factibilidad de instalación electrica?',
            color: 'geekblue',
            name:'electric_found',
            suffix: 'SI/NO',
            value: state.wells.temporary_well.well_data.has_flow_sensor.value
        }
    ]

    const addValue = (name, value) => {          
        
        dispatch({
            type:'ADD_FIELD_WELL_DATA',
            field: name,
            value: name !== 'has_flow_sensor' ?  parseFloat(value).toFixed(2): value,
            select: true
        })
    }

    const onBlur = (name, value) => {                  
        dispatch({
                type:'ADD_FIELD_WELL_DATA',
                field: name,
                value:parseFloat(value).toFixed(2),            
                select: false
            })
    }
    
    
    return(<Card hoverable title={state.wells.temporary_well.is_edit ? <> Edita los valores para el pozo <b>{state.wells.temporary_well.general_data.name_well}</b></>:'Ingresa aquí los datos de tu pozo...'}>        
        
        {data.map((item, index)=> {
            return(<Row>
                    <Col span={item.color==='blue' ?  window.innerWidth > 800 ? 2:2:2} style={{marginTop:'15px', marginBottom:'15px'}}>                        
                        <Tag style={{marginTop:item.color==='geekblue'&& '0px'}} color={item.color}>{index+1}) {item.title}</Tag>                                                
                    </Col>
                    <Col span={item.color==='blue' ? window.innerWidth > 800 ? 5:12:12} offset={item.color==="blue" ? window.innerWidth>800?17:17:17} style={{marginTop: item.color==='blue' ?'10px':'-10px', marginBottom:'0px'}}>
                        {item.color==='geekblue' ? <> 
                        <Select size='small' onSelect={(value)=> {                            
                            if(item.name==="has_flow_sensor"){ 
                                console.log(value)
                                if(value=='SI'){
                                    setIsFlow(true)
                                    console.log('asd')
                                } else {
                                    setIsFlow(false)

                                }
                                
                            }
                        }} defaultValue={item.value} onChange={(x)=>addValue(item.name, x)} style={{width:'100%', textAlign:'center', marginLeft:window.innerWidth>800?'-60px':'0px'}} placeholder='Selecciona una opción'>
                            <Option value='SI'>SI</Option>
                            <Option value='NO'>NO</Option>
                        </Select>
                        {item.name==="has_flow_sensor" & isFlow ? <TextArea rows={3} placeholder='Funciona el sensor?' style={{marginLeft:'-60px'}} />:<></>}
                        </>:<>
                        <Badge.Ribbon text={<>{item.suffix}</>} style={{zIndex:2, marginTop:'-26px', marginRight:window.innerWidth>800?'-2px':'10px', fontSize:'12px'}} />   
                        <Input    
                            onChange={(x)=>addValue(item.name, x)}                         
                            onBlur={(x)=>onBlur(item.name, x.target.value)}
                            defaultValue={item.value}                            
                            step={0.5}                            
                            size='small'
                            min={1.0}
                            max={500.0}
                            style={{width:'80px', textAlign:'center', marginLeft:window.innerWidth>800?'0px':'80px'}}                                                                                    
                        />
                        </>}
                    </Col>
                    
                </Row>)
        })}
        {window.innerWidth <800 && <Col>
            {state.wells.temporary_well.is_edit ? <>                     
                    {state.wells.temporary_well.images  ? 
                    <Button type='primary' style={{marginRight:'10px'}} icon={<FileImageFilled />} onClick={()=> activeImg('a') } >                        
                        Imágenes
                    </Button>:
                    <Button type='primary' style={{marginRight:'10px'}} icon={<FileImageFilled />} onClick={()=> activeImg('a') } >                        
                        Imágenes
                    </Button>}
                    <Button type='primary' icon={<ArrowRightOutlined />} onClick={()=> activeImg() } >
                        Actualizar! y ver pozos                   
                    </Button>
                </>:<Popconfirm onCancel={()=>activeImg()} onConfirm={()=>activeImg('a')} style={{zIndex:2}} title="¿Quieres agregar imágenes?" okText='SI, agregar imágenes' cancelText="NO, continuar sin imágenes">                
                    <Button type='primary' icon={<ArrowRightOutlined />} >
                        Siguiente!                    
                    </Button>
                </Popconfirm>}                
            </Col>}        
    </Card>)

}


export default ListFormDataWell