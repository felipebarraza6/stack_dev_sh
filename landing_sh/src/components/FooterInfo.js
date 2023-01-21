import React from 'react'
import { Row, Col, Typography } from 'antd'
import logo from '../assets/images/logo2.png'
import FormSuscription from './FormSuscription'
const { Paragraph, Title } = Typography

const FooterInfo = () => {

    return(<Row justify='center' style={{backgroundColor:'#1F3461'}}>
        <Col xs={24} sm={12} md={12} lg={6} xl={12} style={{padding:'20px'}}>
            
                <center><img alt='logo' src={logo} width='250px' style={{marginBottom:'20px'}} /></center>
                <Paragraph align='justify' style={{color:'white'}}>Somos una Startup de innovación socio-ambiental, con la misión de garantizar el uso sostenible del recurso hídrico, 
                    entregar soluciones con garantía de calidad y a la vanguardia tecnológica. Atendemos a organizaciones y empresas que 
                    emplean el recurso hídrico en sus operaciones a través de servicios de ingeniería, telemetría y análisis de agua. Siempre 
                    en armonía con el medio ambiente y en cumplimiento con las normativas y resoluciones vigentes.</Paragraph>
            
        </Col>
        <Col xs={24} sm={12} md={12} lg={6} xl={12} style={{paddingLeft:'20px',paddingRight:'20px', paddingBottom:'20px'}}>
            <center><Title style={{color:'white', marginBottom:'-30px', marginTop:'20px'}}>CONTACTO</Title></center>
            <FormSuscription />
        </Col>       
    </Row>)
}


const styles = {
    a: {
        color:'black'
    }
}

export default FooterInfo
