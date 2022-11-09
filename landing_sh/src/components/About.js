import React from 'react'
import { Col, Row, Typography } from 'antd'
import Lines from '../assets/images/elements/lines.png'
const { Title, Paragraph } = Typography


const About = () => {

    return(
        <Row style={{marginLeft:window.innerWidth > 1000 ? '240px':'0px', padding: window.innerWidth < 800 && '20px', marginBottom: window.innerWidth < 800 && '50px'}}>
            <Col xl={10} xs={24} md={24} style={styles.colPara}>
              <Title bold style={styles.title}>Misión</Title>
                <Paragraph style={styles.paragraph} align='justify' >
                    Somos una Startup de innovación socio-ambiental, con la misión de garantizar el uso sostenible
                    del recurso hídrico, entregar soluciones con garantía de calidad y a la vanguardia tecnológica. 
                    Atendemos a organizaciones y empresas que emplean el recurso hídrico en sus operaciones a través 
                    de servicios de ingeniería, telemetría y análisis de agua. Siempre en armonía con el medio ambiente 
                    y en cumplimiento con las normativas y resoluciones vigentes.
                </Paragraph>
            </Col>
            <Col xl={4} xs={24} md={0}  style={{marginLeft:'-100px'}}>
                {window.innerWidth > 900 && <img src={Lines} width='120%' />}
            </Col>
            <Col xl={10} xs={24} md={24} style={{paddingTop:'50px', paddingLeft: window.innerWidth > 1000 && '50px'}}>
                <Title style={styles.title}>Visión</Title>
                <Paragraph style={styles.paragraph} align='justify'>                  
                    Ser el referente en la sustentabilidad y eficiencia hídrica en Sudamérica en los próximos 3 años 
                    a través de procesos de innovación en los servicios entregados, en la gestión empresarial y la creación 
                    de valor para nuestros clientes.
                </Paragraph>
            </Col>

        </Row>
    )
}


const styles = {    
    title: {        
        textAlign:'center'
    },
    paragraph: {        
        padding:'20px'
    },
    colPara: {
        paddingTop: '50px',        
    }
}


export default About
