import React from 'react'
import { Row, Col, Card, Typography, Button } from 'antd'
import wall_webinars from '../../assets/images/wallpaper_webinars.jpeg'
import cris from '../../assets/images/cris.jpg'
const { Title, Paragraph, Text } = Typography


const WebinarsDemo = () => {

  return(<>
      
          <Col span={12}>
              <img src={wall_webinars} style={{width:"100%", marginTop: '15px'}} />
          </Col>
          <Col span={12}>
              <Card>
                <Row>
                  <Col span={10}>
                    <img src={cris} style={{width:"80%", border: '3px solid #1890ff', borderRadius: '8px', marginTop:'0px', marginBottom: '20px'}} />
                    <Text style={{marginLeft:'42px'}} strong>Christian Fernández</Text><br />

                    <Paragraph style={{marginRight:'18px', marginLeft:'5px'}}>Líder en soluciones hídricas par el sector agroindustrial</Paragraph>
                  </Col>
                  <Col span={12} style={{backgroundColor:'white', paddingTop:'0px'}}>
                    <Title level={4}>WEBINAR; Cumplimiento Resolución MEE_DGA N°1.238</Title>
                    <Title level={5}>Monitoreo para extracciones efectivas de aguas subterráneas y superficiales</Title>
                    <Paragraph align='justify'>Smart Hydro tiene el agrado de invitarlos a participar en nuestro Webinar de “(MEE) Monitoreo de Extracciones Efectivas para aguas subterráneas y superficiales”. El cual busca informar y contextualizar sobre la resolución impuesta por la DGA para enfrentar la escasez hídrica que sufre el país.</Paragraph>
                    <Text mark>Martes 23 de Agosto a las 15:00 hrs.</Text><br /><br />
                    <Paragraph style={{color:'grey'}}>El registro e ingreso al Webinar, se habilitara 30 minutos previos a la fecha y hora de inicio programada.</Paragraph>                     
                    <Button type='primary' disabled >REGISTRARSE PARA INGRESAR</Button>
                  </Col>
                </Row>
              </Card>
          </Col>      
  </>)

}


export default WebinarsDemo
