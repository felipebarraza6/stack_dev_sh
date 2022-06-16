import React from 'react'
import { Col, Row, Typography } from 'antd'
const { Title, Paragraph, Text } = Typography


const About = () => {

    return(
        <Row style={styles.container} >
            <Col xs={24} sm={12} md={12} lg={12} xl={12} style={styles.colPara}>
              <Title style={styles.title}>Misión</Title>
                <Paragraph style={styles.paragraph} align='justify'>
                
                <Text style={{color: 'white'}}>
      Somos una Startup de innovación socio-ambiental, con la misión de garantizar el uso sostenible del recurso hídrico, entregar soluciones con garantía de calidad y a la vanguardia tecnológica. Atendemos a organizaciones y empresas que emplean el recurso hídrico en sus operaciones a través de servicios de ingeniería, telemetría y análisis de agua. Siempre en armonía con el medio ambiente y en cumplimiento con las normativas y resoluciones vigentes.
                </Text>

                </Paragraph>
            </Col>
            <Col xs={24} sm={12} md={12} lg={12} xl={12} style={styles.colPara}>
<Title style={styles.title}>Visión</Title>
                <Paragraph style={styles.paragraph} >
                    <Text style={{color: 'white'}}>                        
      Ser el referente en la sustentabilidad y eficiencia hídrica en Sudamérica en los próximos 3 años a través de procesos de innovación en los servicios entregados, en la gestión empresarial y la creación de valor para nuestros clientes


                    </Text>
                </Paragraph>
            </Col>

        </Row>
    )
}


const styles = {
    container: {
        paddingTop: '80px',
        paddingLeft: '10px',
        paddingRight: '10px',
        paddingBottom: '40px',
        backgroundColor: '#002766',
    },
    title: {
        color: 'white',
        marginLeft: '20px'
    },
    paragraph: {
        color: 'white'

    },
    colPara: {
        padding: '40px'        
    },
    dates: {
        textAlign: 'right',
        color: 'red',
        paddingRight: '20px',
        fontSize: '20px',        
    },
    textDates: {
        color: 'white',
    }
}


export default About
