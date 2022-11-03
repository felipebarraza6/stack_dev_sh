import React, { useContext,  } from 'react'
import { Badge, Row, Col, Button, Popconfirm, notification } from 'antd'
import { QuotationContext } from '../../../containers/Quotation'
import { ArrowRightOutlined, FileImageFilled } from '@ant-design/icons'

import img_well from '../../../assets/images/dem1.png'


const WellDisplay = () => {

    const { state, dispatch } = useContext(QuotationContext)    
    
    const granted_flow = state.wells.temporary_well.well_data.granted_flow
    const well_depth= state.wells.temporary_well.well_data.well_depth
    const static_level= state.wells.temporary_well.well_data.static_level
    const dynamic_level=state.wells.temporary_well.well_data.dynamic_level
    const pump_installation_depth=state.wells.temporary_well.well_data.pump_installation_depth
    const inside_diameter_well=state.wells.temporary_well.well_data.inside_diameter_well
    const duct_outside_diameter=state.wells.temporary_well.well_data.duct_outside_diameter

    const styles = {
        colWell: {
            backgroundImage:`url(${img_well})`,
            backgroundPosition: 'center',
            backgroundSize: '170%',                
            height: '550px',
            position:'absolute',                
            backgroundRepeat: 'no-repeat',
            width: '120%', zIndex:2
        },
        baseBadge: {

        }
    }

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
    


    return(<>
        <Row justify='end'>                    
            <Col span={24} style={styles.colWell}>   
                    <Badge                     
                        style={{                        
                            backgroundColor: !granted_flow.select ? 'white':'#1890ff', 
                            color: !granted_flow.select ? '#1890ff':'white',
                            borderColor: !granted_flow.select ? '#1890ff':'white',
                            fontSize: granted_flow.select && '15px',
                            marginRight:'-195px',
                            marginTop:'125px', 
                            position:'absolute'
                        }} count={`1) ${granted_flow.value} (Mt)`} />

                    <Badge                     
                    style={{
                        backgroundColor: !well_depth.select ? 'white':'#1890ff', 
                        color: !well_depth.select ? '#1890ff':'white',
                        borderColor: !well_depth.select ? '#1890ff':'white',
                        fontSize: well_depth.select && '15px',
                        marginRight:'-230px',
                        marginTop:'310px', 
                        position:'absolute'
                    }} count={`2) ${well_depth.value} (Mt)`} />
                    <Badge                     
                        style={{
                            backgroundColor: !static_level.select ? 'white':'#1890ff', 
                            color: !static_level.select ? '#1890ff':'white',
                            borderColor: !static_level.select ? '#1890ff':'white',
                            fontSize: static_level.select && '15px',
                            marginRight:'-400px',
                            marginTop:'280px', 
                            position:'absolute'
                        }}                    
                        count={`3) ${static_level.value} (Mt)`} />
                    <Badge                     
                        style={{
                            backgroundColor: !dynamic_level.select ? 'white':'#1890ff', 
                            color: !dynamic_level.select ? '#1890ff':'white',
                            borderColor: !dynamic_level.select ? '#1890ff':'white',
                            fontSize: dynamic_level.select && '15px',
                            marginRight:'-405px',
                            marginTop:'320px', 
                            position:'absolute'
                        }}                    
                        count={`4) ${dynamic_level.value} (Mt)`} />
                    <Badge                     
                        style={{
                            backgroundColor: !pump_installation_depth.select ? 'white':'#1890ff', 
                            color: !pump_installation_depth.select ? '#1890ff':'white',
                            borderColor: !pump_installation_depth.select ? '#1890ff':'white',
                            fontSize: pump_installation_depth.select && '15px',
                            marginRight:'-390px',
                            marginTop:'400px', 
                            position:'absolute'
                        }}                    
                        count={`5) ${pump_installation_depth.value} (Mt)`} />
                    <Badge                     
                        style={{
                            backgroundColor: !inside_diameter_well.select ? 'white':'#1890ff', 
                            color: !inside_diameter_well.select ? '#1890ff':'white',
                            borderColor: !inside_diameter_well.select ? '#1890ff':'white',
                            fontSize: inside_diameter_well.select && '15px',
                            marginRight:'-445px',
                            marginTop:'175px', 
                            position:'absolute'
                        }}                    
                        count={`6) ${inside_diameter_well.value} (MM/PULG)`} />
                    <Badge                     
                        style={{
                            backgroundColor: !duct_outside_diameter.select ? 'white':'#1890ff', 
                            color: !duct_outside_diameter.select ? '#1890ff':'white',
                            borderColor: !duct_outside_diameter.select ? '#1890ff':'white',
                            fontSize: duct_outside_diameter.select && '15px',
                            marginRight:'-410px',
                            marginTop:'120px', 
                            position:'absolute'
                        }}                    
                        count={`7) ${duct_outside_diameter.value} (MM/PULG)`} />                
            </Col>       
            
        </Row>
        <Row >
            <Col style={{ paddingLeft:state.wells.temporary_well.is_edit ? 
                    state.wells.temporary_well.is_load_image ? 
                        '24%':'25%' :'69%', 
                    paddingTop:'110%', zIndex:10}}>
                                
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
                
            </Col>
        </Row>
    </>)

}


export default WellDisplay