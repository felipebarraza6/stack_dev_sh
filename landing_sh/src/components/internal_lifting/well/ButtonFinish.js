import React, { useContext, useState } from 'react'

import { QuotationContext } from '../../../containers/Quotation'
import { InternalLiftingContext } from '../../pages/InternalLifting'
import { Button, Modal, Typography, Spin, Row, Col, notification } from 'antd'
import { SendOutlined  } from '@ant-design/icons'
import { callbacks } from '../../../api/endpoints'


const ButtonFinish = () => {
    const { state, dispatch } = useContext(InternalLiftingContext)

    const [apiState, setApiState] = useState({
        client: {
            id: null
        },
        quotation: {
            uuid: null
        }
    })

    const [visible, setVisible] = useState(false)

    
    

    const senData = async() => {
        setVisible(true)
        console.log(state.wells.list)
        const rq1_create_client = await callbacks.external_clients.create({...state.client}).then((response)=>{            
            notification.success({message: 'DATOS DE CONTACTO'})           
            const rq2_create_quotation =  callbacks.quotation.create({
                external_client: response.data.id,
                is_external_client: true,            
            }).then((response)=>{                
                notification.success({message: `${response.data.uuid} ID UNICO EN NUESTRA API`})           
                var list_with_quotation_uui = (list) => {
                    var list_f = []            
                    list.map((well)=> {
                        list_f.push({
                            ...well,
                            quotation: response.data.uuid
                        })
                    })            
                    return list_f            
                }
        
                const r3_create_wells = callbacks.quotation.createWell(list_with_quotation_uui(state.wells.list)).then((r)=> {
                    setTimeout(() => {
                        window.location.assign('/')
                    }, 5000);
                })
            })
        })
    }


    return (<>
            <Modal visible={visible} onCancel={()=>setVisible(false)} footer={[]} width={'650px'} centered>
                <Row justify="center">
                    <Col span={24}>
                        <center><Typography.Title level={3}>
                        DATOS CARGADOS CORRECTAMENTE, TE ENVIAREMOS UNA COTIZACION A LA BREVEDAD...
                        </Typography.Title></center>
                    </Col>
                    <Col span={24} style={{marginLeft:'95%', marginTop:'40px', marginBottom:'40px'}}>
                        <Spin size='large' />                        
                    </Col>
                    <Col span={24}><center>
                        <Typography.Title level={5}>Estamos procesando tu información... serás redirigido a <a>https://smarthydro.cl</a> en cuanto termine!</Typography.Title>
                        </center>
                    </Col>
                </Row>
            </Modal>
            <Button 
                type='primary' 
                icon={<SendOutlined />} 
                onClick={()=>dispatch({type:'SET_CURRENT', step:3})} >Siguiente</Button></>)

}


export default ButtonFinish