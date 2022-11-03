import React, { useContext, useState, useEffect } from 'react'
import { Row, Col, Typography, 
        Upload, Card, Button,
        notification, Tooltip } from 'antd'
import { PlusOutlined, CloseOutlined, ArrowLeftOutlined, ArrowRightOutlined } from '@ant-design/icons'
import r1 from '../../../assets/images/referencia/general.png'
import r2 from '../../../assets/images/referencia/detalle_salida_pozo.png'
import { QuotationContext } from '../../../containers/Quotation'

const { Title, Paragraph, Text } = Typography

const ImageLoader = () => {

    const { state, dispatch } = useContext(QuotationContext)

    const [img1, setImg1] = useState(null)
    const [img2, setImg2] = useState(null)

    useEffect(() => {
        if(state.wells.temporary_well.is_edit){ 
            if(state.wells.temporary_well.images){
                setImg1(state.wells.temporary_well.images.r1)
                setImg2(state.wells.temporary_well.images.r2)
            }                       
            
        }

    }, [])

    const changeCurrent = () => {

        dispatch({
            type: 'SET_CURRENT',
            step: 1
        })
        dispatch({
            type: 'SET_STEP_03',
            active: true,
            finish: true,
            hide: true,
            is_load_image: state.wells.temporary_well.is_edit ?  img1 & img2 ? true:false:false
        })
    }    
 

    const addImages = () => {
        if(img1 || img2){            
            dispatch({
                type: 'SET_STEP_03',
                active: true,
                finish: true,
                hide: true,
                is_load_image: false
            })
            if(!state.wells.temporary_well.is_edit){
                dispatch({
                    type: 'ADD_WELL_CONFIRM',
                    well: {...state.wells.temporary_well, images: { r1:img1, r2:img2 }}
                  })
            notification.success({message:'Pozo agregado correctamente...'})
            }else{
                dispatch({
                    type: 'UPDATE_WELL',
                    well: {...state.wells.temporary_well, images: { r1:img1, r2:img2 }}
                })
                notification.success({message:'Pozo actualizado correctamente...'})
            }
            
        } else{
            notification.error({message:'Debes ingresar al menos una imágen...'})
        }

        
    }

    return(<Row style={styles.container}>
        <Col span={24}>
        <Card style={{paddingBottom:'50px'}} title={<Row>
            <Col span={window.innerWidth > 800 ? 4:24} style={{marginBottom:window.innerWidth <800&&'10px'}}>
            <Button icon={<ArrowLeftOutlined/>} type='primary' style={{marginRight:'10px', backgroundColor:'#d6e4ff', color:'black'}} onClick={changeCurrent}>VOLVER AL POZO</Button>
            </Col>
            <Col span={window.innerWidth > 800 ? 20:24}>
            <Button type='primary' onClick={addImages} >FINALIZAR REGISTRO DE IMÁGENES <ArrowRightOutlined/></Button>            
            </Col>
            </Row>}>
            <Row>
                <Col span={24} style={{marginBottom:'20px'}}>            
                        <Title style={styles.title} level={4}>Agrega tus imágenes de refencia (opcional)</Title>
                </Col>
                <Col span={window.innerWidth>800?12:24}>
                    <Col span={window.innerWidth > 800 ? 12:24}>                    
                        <img src={r1} width={'100%'} style={{borderRadius:'10px'}} />
                    </Col>
                    <Col span={window.innerWidth > 800 ? 12:24} style={{padding:'10px'}}>
                        <Title level={5}>GENERAL</Title>
                        <Paragraph style={{marginTop:'20px'}}>HAZ CLICK EN EL SÍMBOLO (+) PARA SUBIR LA IMÁGEN GENERAL</Paragraph>
                        {img1 && <Tooltip title='ELIMINAR ARCHIVO'>
                            <Button onClick={()=>setImg1(null)} type='primary' icon={<CloseOutlined />}>{img1.name.slice(0,15)}...</Button>
                        </Tooltip>}
                    </Col>
                    <Col span={12} style={{marginBottom:'20px'}}>
                        <Upload name="r1" listType="picture-card" showUploadList={false} maxCount={1} 
                            onChange={(e)=> setImg1(e.file.originFileObj)} ><PlusOutlined />
                        </Upload>
                    </Col>
                </Col>
                <Col span={window.innerWidth>800?12:24}>
                    <Col span={window.innerWidth > 800 ? 12:24}>                    
                        <img src={r2}  width={'100%'} style={{borderRadius:'10px'}} />                                         
                    </Col>
                    <Col span={window.innerWidth > 800 ? 12:24} style={{padding:'10px'}}>
                        <Title level={5}>DETALLE DE SALIDA DE POZO</Title>
                        <Paragraph style={{marginTop:'20px'}}>HAz CLICK EN EL SÍMBOLO (+) PARA SUBIR LA IMÁGEN DE DETALLE DE SALIDA DE POZO</Paragraph>
                        {img2 && <Tooltip title='ELIMINAR ARCHIVO'>
                            <Button onClick={()=>setImg2(null)} type='primary' icon={<CloseOutlined />}>{img2.name.slice(0,15)}...</Button>
                        </Tooltip>}
                        <Col span={12}>
                        <Upload name="r2" listType="picture-card" showUploadList={false} maxCount={1} 
                            onChange={(e)=> setImg2(e.file.originFileObj)} ><PlusOutlined />
                        </Upload>
                        </Col>
                    </Col>
                </Col>
            </Row>                  
        </Card>
        </Col>
    </Row>)
}

const styles = {
    title: {
        marginBottom: '20px',
    },
    container: {
        marginLeft:'15px',
        marginRight:'15px',
        marginTop:'15px',        
    }
}

export default ImageLoader