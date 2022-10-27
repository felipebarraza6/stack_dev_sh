import React, { useContext } from 'react'
import { Timeline, Tag, Typography, 
            Button, Row, Col,
            Collapse } from 'antd'    
import { CheckCircleFilled } from '@ant-design/icons'
import { QuotationContext } from '../../containers/QuotationExternalClients'


const { Item } = Timeline
const { Paragraph } = Typography 

const { Panel } = Collapse

const TimeLineProcess = () => {

    const { state, dispatch } = useContext(QuotationContext)
    const validated_info = state.validated_info
    const client = state.client

    function editClient(){
        dispatch({
            type:'SET_CURRENT',
            step: 0
        })
    }    

    return(<Timeline style={styles.timeline}>
        {validated_info.client_info ? 
            <Item color='green' dot={<CheckCircleFilled />}>
                <Paragraph>Datos de contacto</Paragraph>
                    <Row>                    
                        <Col span={24}>
                            <Tag color={'geekblue'} style={styles.tagClient}>{client.name_enterprise}</Tag>
                        </Col>
                        <Col span={24}>
                            <Tag color={'geekblue'} style={styles.tagClient}>{client.name_contact}</Tag>
                        </Col>
                        <Col span={24}>
                            <Tag color={'geekblue'} style={styles.tagClient}>{client.mail_contact}</Tag>
                        </Col>
                        <Col span={24}>
                            <Tag color={'geekblue'} style={styles.tagClient}>{client.phone_contact}</Tag>
                        </Col>
                    </Row>
                    <div style={styles.containerBtn}>
                        <Button size='small' onClick={editClient} type='primary'>Editar datos de contacto</Button>
                    </div>                    
            </Item>:
            <Item color='red'>
                Aún no has ingresado tus datos de contacto
            </Item>}  
        {state.counter_wells > 0 ? 
            <Item> Has ingresado {state.counter_wells} pozos</Item>:
            <Item color="red">No hay pozos ingresados</Item>
        }      
    </Timeline>)

}

const styles = {
    timeline: {
        backgroundColor: 'white',
        paddingTop:'20px',
        paddingLeft:'12px',
        height:'100%',                
    },
    tagClient: {
        margin:'4px'
    },
    containerBtn: {
        marginLeft:'5px',
        marginTop:'5px'
    }
}

export default TimeLineProcess