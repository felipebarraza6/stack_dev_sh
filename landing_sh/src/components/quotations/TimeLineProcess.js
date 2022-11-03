import React, { useContext } from 'react'
import { Timeline, Tag, Typography, 
            Button, Row, Col,
            Collapse, Tooltip, Alert } from 'antd'    
import { CheckCircleFilled, CheckSquareFilled,  LoadingOutlined, CloseSquareFilled, EditOutlined } from '@ant-design/icons'
import { QuotationContext } from '../../containers/Quotation'


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
                            {client.mail_contact.length > 25 ?
                                <Tooltip title={client.mail_contact} color='geekblue'>
                                    <Tag color={'geekblue'} style={styles.tagClient}>{client.mail_contact.slice(0,25)}...</Tag>
                                </Tooltip>:<Tag color={'geekblue'} style={styles.tagClient}>{client.mail_contact.slice(0,25)}</Tag>
                            }                            
                        </Col>
                        <Col span={24}>
                            <Tag color={'geekblue'} style={styles.tagClient}>{client.phone_contact}</Tag>
                        </Col>
                    </Row>
                    <div style={styles.containerBtn}>
                        <Button size='small' onClick={editClient} type='primary' icon={<EditOutlined/>}>Editar</Button>
                    </div>                    
            </Item>:
            <Item color='red'>
                Aún no has ingresado tus datos de contacto                
                <br/>
                <br/>
                <Paragraph style={{paddingLeft:'10px'}}><CloseSquareFilled style={{color:'red'}} /> Nombre </Paragraph>
                <Paragraph style={{paddingLeft:'10px'}}><CloseSquareFilled style={{color:'red'}} /> Nombre Contacto</Paragraph>
                <Paragraph style={{paddingLeft:'10px'}}><CloseSquareFilled style={{color:'red'}} /> Email Contacto</Paragraph>
                <Paragraph style={{paddingLeft:'10px'}}><CloseSquareFilled style={{color:'red'}} /> Teléfono Contacto</Paragraph>
            </Item>}  
        {state.wells.temporary_well.general_data && <Item dot={<LoadingOutlined />}>
                    <Paragraph>{state.wells.temporary_well.is_edit ? <>Estás editando el pozo: <u><b>{state.wells.temporary_well.general_data.name_well}</b></u></>:'Estás agregando un pozo'}</Paragraph>
                    <Row>                    
                        <Col span={24}>
                            <Tag color={'green'} style={styles.tagClient}>{state.wells.temporary_well.general_data.name_well.toUpperCase()}</Tag>
                        </Col>
                        <Col span={24}>
                        <Tag color={'green'} style={styles.tagClient}>{state.wells.temporary_well.general_data.type_captation.toUpperCase()}</Tag>
                        </Col>
                        <Col span={24}>
                            <Paragraph style={{paddingLeft:'10px'}}>
                                {state.wells.temporary_well.general_data.address_exact.toUpperCase()}
                            </Paragraph>
                        </Col>                        
                        <Col span={24}>     
                        <Collapse ghost={true} style={{marginTop:'-15px',marginLeft:'-10px'}} defaultActiveKey	={['1']}>
                        <Panel key="1" header="DATOS">
                            <Paragraph style={{paddingLeft:'25px', marginTop:'-20px'}}>
                                1) {parseFloat(state.wells.temporary_well.well_data.granted_flow.value).toFixed(2)} {state.wells.temporary_well.well_data.granted_flow.value > 0 ? <CheckSquareFilled style={{color:'green'}} />:<CloseSquareFilled style={{color:'red'}} />}<br />                                
                                2) {parseFloat(state.wells.temporary_well.well_data.well_depth.value).toFixed(2)} {state.wells.temporary_well.well_data.well_depth.value > 0 ? <CheckSquareFilled style={{color:'green'}} />:<CloseSquareFilled style={{color:'red'}} />}<br />
                                3) {parseFloat(state.wells.temporary_well.well_data.static_level.value).toFixed(2)} {state.wells.temporary_well.well_data.static_level.value > 0 ? <CheckSquareFilled style={{color:'green'}} />:<CloseSquareFilled style={{color:'red'}} />}<br />
                                4) {parseFloat(state.wells.temporary_well.well_data.dynamic_level.value).toFixed(2)} {state.wells.temporary_well.well_data.dynamic_level.value > 0 ? <CheckSquareFilled style={{color:'green'}} />:<CloseSquareFilled style={{color:'red'}} />}<br />
                                5) {parseFloat(state.wells.temporary_well.well_data.pump_installation_depth.value).toFixed(2)} {state.wells.temporary_well.well_data.pump_installation_depth.value > 0 ? <CheckSquareFilled style={{color:'green'}} />:<CloseSquareFilled style={{color:'red'}} />}<br />
                                6) {parseFloat(state.wells.temporary_well.well_data.inside_diameter_well.value).toFixed(2)} {state.wells.temporary_well.well_data.inside_diameter_well.value > 0 ? <CheckSquareFilled style={{color:'green'}} />:<CloseSquareFilled style={{color:'red'}} />}<br />
                                7) {parseFloat(state.wells.temporary_well.well_data.duct_outside_diameter.value).toFixed(2)} {state.wells.temporary_well.well_data.duct_outside_diameter.value > 0 ? <CheckSquareFilled style={{color:'green'}} />:<CloseSquareFilled style={{color:'red'}} />}<br />
                                8) {state.wells.temporary_well.well_data.has_flow_sensor.value ? state.wells.temporary_well.well_data.has_flow_sensor.value: <>SIN RESPUESTA <CloseSquareFilled style={{color:'red'}} /></> } 
                            </Paragraph>
                        </Panel>                        
                            </Collapse>                       
                        </Col>         
                    </Row>                        
        </Item>}
        {state.counter_wells > 0 ? 
            <Item> 
                <Paragraph>Haz ingresado <b>{state.counter_wells}</b> {state.counter_wells>1 ? 'pozos':'pozo' } </Paragraph>
                {state.wells.list.map((x, index)=><>
                    <Paragraph>
                        {index+1}) <b>{x.general_data.name_well.toUpperCase()}</b>
                    </Paragraph>
                    <Paragraph style={{marginLeft:'18px', marginTop:'-20px'}}>
                        {x.general_data.address_exact.toUpperCase()}
                    </Paragraph>

                </>)}

            </Item>:
            <Item color="red">
                <Paragraph>No hay pozos ingresados</Paragraph>
                <Alert style={{marginRight:'10px'}} message={'Debes comenzar agregando los datos iniciales de tu primer pozo...'} type='error' />
            </Item>
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