import React, { useContext } from 'react'
import { QuotationContext } from '../../../containers/Quotation'
import { InternalLiftingContext } from '../../pages/InternalLifting'
import { PlusCircleFilled, SendOutlined, EditOutlined,  } from '@ant-design/icons'
import ImageLoader from './ImageLoader'
import { Result, Button, Row, 
    Col, Table, Typography, 
    Tag, Tooltip, Popconfirm } from 'antd'

import ButtonFinish from './ButtonFinish'

const { Title } = Typography

const ImageOrFinish = () => {

    const { state, dispatch } = useContext(InternalLiftingContext)

    return(<>
        {state.wells.temporary_well.is_load_image ? 
            <ImageLoader />:<Row  style={{paddingBottom:state.wells.list.length == 1 ? '17%': state.wells.list.length ==2 ? '10%':'0%', marginTop:window.innerWidth>900&&'100px'}}>
            
            <Col span={window.innerWidth > 800 ? 15:24} style={{paddingLeft:'10px'}}>
                {state.wells.list.length>0 &&
                    <Table bordered dataSource={state.wells.list} title={()=><Title level={4}>Listado de pozos ingresados correctamente</Title>} 
                        columns={[
                            {
                                title:'Datos generales',
                                render: (x)=><>
                                    <Tag color="blue" style={{marginBottom:'5px'}}>{x.general_data.name_well.toUpperCase()}</Tag><br />
                                    <Tag color="geekblue" style={{marginBottom:'5px'}}>{x.general_data.type_captation.toUpperCase()}</Tag><br />
                                    {x.general_data.address_exact.length>15 ?
                                        <Tooltip title={x.general_data.address_exact} color="purple">
                                            <Tag color="purple" style={{marginBottom:'5px'}}>{x.general_data.address_exact.toUpperCase().slice(0,15)}...</Tag><br />
                                        </Tooltip>:<><Tag color="purple" style={{marginBottom:'5px'}}>{x.general_data.address_exact.toUpperCase().slice(0,15)}...</Tag><br /></>
                                    }
                                    
                                </>
                            },                                                        
                            {
                                title:'Datos del pozo',
                                render: (x)=><>
                                    <u>{window.innerWidth>800?'Caudal otorgado':'1)'}:</u> {x.well_data.granted_flow.value}<br />
                                    <u>{window.innerWidth>800?'Profundidad del pozo':'2)'}:</u> {x.well_data.well_depth.value}<br />
                                    <u>{window.innerWidth>800?'Nivel estático':'3)'}:</u> {x.well_data.static_level.value}<br />
                                    <u>{window.innerWidth>800?'Nivel dinámico':'4)'}:</u> {x.well_data.dynamic_level.value}<br />
                                    <u>{window.innerWidth>800?'Profundidad instalación bomba':'5)'}:</u> {x.well_data.pump_installation_depth.value}<br />
                                    <u>{window.innerWidth>800?'Diámetro interior pozo':'6)'}:</u> {x.well_data.inside_diameter_well.value}<br />
                                    <u>{window.innerWidth>800?'Diámetro exterior ducto salida bomba':'7)'}:</u> {x.well_data.duct_outside_diameter.value}<br />
                                </>
                            },
                            {                             
                                render: (x)=><>
                                    <Button type='primary' onClick={()=>{
                                        console.log(x)
                                        x = {
                                            ...x,
                                            is_edit:true
                                        }                                        
                                        dispatch({type:'SELECT_EDIT_WELL', well:x})
                                        dispatch({type:'SET_CURRENT', step:0})
                                        
                                        }} style={{marginRight:'5px', marginBottom:window.innerWidth<800&&'10px'}} icon={<EditOutlined />} >Editar</Button>  
                                        <Popconfirm okText='SI, eliminar' cancelText='NO' onConfirm={()=> dispatch({type:'DELETE_WELL', well:x})} title='¿Estás seguro de eliminar este pozo? se perderá toda la información ingresada.'>
                                            <Button type='primary' danger  >Eliminar</Button>
                                    </Popconfirm>                                  
                                </>
                            }
                        ]}
                        pagination={{ defaultPageSize: 2}}
                    />            
                }
            </Col>
            <Col span={state.wells.list.length > 0 ? window.innerWidth > 800 ? 9:24:24}>                
            <Result
                status="success"
                title="Haz realizado el ingreso correctamente!"
                subTitle="Pozo ingresado correctamente con toda su información..."                
                extra={[                
                <Button key="buy" onClick={()=>{
                    dispatch({type:'RESET_TEMPORARY_WELL'})
                    dispatch({type:'SET_CURRENT', step:0})
                    dispatch({
                        type:'SET_STEP_03',
                        hide: true
                    })
                }} icon={<PlusCircleFilled style={{color:'#1890ff', fontSize:'15px'}} />}>Ingresar un nuevo pozo</Button>,<>
                {state.wells.list.length > 0 &&
                <ButtonFinish />}</>
                ]}
            />
            </Col>
            
            </Row>
        }
    </>)

}


export default ImageOrFinish