import React from 'react'
import { Row, Col, Typography,
        Card } from 'antd'
import { CalendarOutlined, DesktopOutlined,
        DeploymentUnitOutlined, BuildOutlined, TeamOutlined,
        InfoCircleFilled, WifiOutlined, ExperimentOutlined } from '@ant-design/icons'

const { Title } = Typography

const Services = () => {

    return(<>
        <Row justify="center" style={styles.row}>
            <Col span={24} style={styles.titleCol}>
                <Title>Que Hacemos</Title>
            </Col>
            <Col style={styles.col} >
                <Card style={styles.card1} hoverable>
                    <BuildOutlined style={styles.icon} />
                    <p>
                        Monitoreo de Extracción  Efectiva de agua 
                        subterránea (MEE /DGA N°1.238).
                    </p>
                </Card>
            </Col>
            <Col style={styles.col} >
                <Card style={styles.card} hoverable>
                    <BuildOutlined style={styles.icon} />
                    <p>
                      Servicio de transmisión de la información 
                      para el cumplimiento Res. MEE 1.238 DGA.
                    </p>
                </Card>
            </Col>
            <Col style={styles.col} >
                <Card style={styles.card1} hoverable>
                    <WifiOutlined style={styles.icon} />
                    <p>
                      Monitoreo y telemetría para Plantas de Agua Potable Rural (APR /SSR).
                    </p>
                </Card>
            </Col>
            

            
        </Row>
        <Row justify='center'>
            <Col style={styles.col}>
                <Card style={styles.card} hoverable>
                    <ExperimentOutlined style={styles.icon} />
                    <p>
                      Muestro y análisis de agua potable según norma NCh 409.
                    </p>
                </Card>
            </Col>
            <Col style={styles.col} >
                <Card style={styles.card1} hoverable>
                    <BuildOutlined style={styles.icon} />
                    <p>
                      Venta de insumos para plantas APR.
                    </p>
                </Card>
            </Col>
            <Col style={styles.col} >
                <Card style={styles.card1} hoverable>
                    <BuildOutlined style={styles.icon} />
                    <p>
                      Diseño y ejecución de sistemas de agua potable.
                    </p>
                </Card>
            </Col>
            <Col style={styles.col} >
                <Card style={styles.card1} hoverable>
                    <BuildOutlined style={styles.icon} />
                    <p>
                      Prueba de bombeo y desarrollo de informe técnico.
                    </p>
                </Card>
            </Col>

        </Row>
        </>
    )
}


const styles = {
    card: {
        width: '250px',        
    },
    
    card1: {
        width: '250px',
        paddingBottom: '20px', 
        "&:hover": {
            background: 'red'
          }
    },    
    card2: {
        width: '250px',
        paddingBottom: '40px'
    },    
    card3: {
        width: '250px',
        paddingBottom: '20px'
    },  
    icon: {
        fontSize: '40px',
        marginBottom: '20px'
    },
    text: {
        fontSize: '22px',
        textAlign: 'center',
    },
    col: {
        textAlign: 'center',
        padding:'20px'
    },
    row: {
        paddingTop:'90px',
        marginBottom: '0px'
    },
    titleCol: {
        textAlign: 'center',
        marginBottom: '35px'
    }
}


export default Services
