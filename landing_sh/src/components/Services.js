import React from 'react'
import { Row, Col, Typography,
        Card, Button } from 'antd'
import { CalendarOutlined, DesktopOutlined,
        CloudOutlined, CloudUploadOutlined, FileDoneOutlined, ShopOutlined,
        ToolOutlined,
        DeploymentUnitOutlined, BuildOutlined, TeamOutlined,
        InfoCircleFilled, WifiOutlined, ExperimentOutlined } from '@ant-design/icons'

import S1 from '../assets/images/services/1.png'
import S2 from '../assets/images/services/2.png'
import S3 from '../assets/images/services/3.png'
import R1 from '../assets/images/services/r1.png'
import R2 from '../assets/images/services/r2.png'
import R3 from '../assets/images/services/r3.png'

import P1 from '../assets/images/services/p1.png'
import P2 from '../assets/images/services/p2.png'
import P3 from '../assets/images/services/p3.png'
import P4 from '../assets/images/services/p4.png'
import P5 from '../assets/images/services/p5.png'

const { Title } = Typography

const Services = () => {

    return(<>
        <Row style={styles.row}>
            <Col span={24} style={styles.titleCol}>
                <Title>Qué puede hacer el <br/> Software(IOT) de Smart Hydro</Title>                
            </Col>
            </Row>  
        <Row justify={'center'} style={{
            
            backgroundImage:`url(${R1})`, 
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'top left',
            backgroundSize:'200px',
            marginLeft:'10px',
            paddingTop:'40px',
            paddingBottom:'20px'
            }}>
            <Col style={styles.col} xl={8} xs={24} md={8}>
                <Card style={styles.card1} hoverable 
                    cover={<img alt="example" style={{padding:'20px'}} src={S1} />} >                                    
                    <p style={{marginTop:'-40px', color:'#FCE921'}}><b>Ayudamos a cumplir con el nuevo estándar ley 20.998</b></p>
                    <Title level={5} style={{marginTop:'-10px', color:'white'}} ><b>¿Que hacemos?</b></Title>
                    <ul style={{marginTop:'-10px', marginLeft:'-30px', marginBottom:'-10px'}}>
                        <li style={{color:'#CBCE07'}}>Medimos de manera remota todas las variables de tu pozo profundo.</li>
                    </ul>
                </Card>
            </Col>
            <Col style={styles.col} xl={8} xs={24} md={8}>
                <Card style={styles.card1} hoverable 
                    cover={<img alt="example" style={{padding:'20px'}} src={S2} />} >                                    
                    <p style={{marginTop:'-40px', color:'#FCE921'}}><b>Apoyamos con el cumplimiento de la norma 1.238</b></p>
                    <Title level={5} style={{marginTop:'-10px', color:'white'}} ><b>¿Cómo lo hacemos?</b></Title>
                    <ul style={{marginTop:'-10px', marginLeft:'-30px', marginBottom:'10px'}}>
                        <li style={{color:'#CBCE07'}}>Generamos la instalación de la implementación exigida por la dirección.</li>
                    </ul>
                </Card>
            </Col>
            <Col style={styles.col} xl={8} xs={24} md={8}>
                <Card style={styles.card1} hoverable 
                    cover={<img alt="example" style={{padding:'20px'}} src={S3} />} >                                    
                    <p style={{marginTop:'-40px', color:'#FCE921'}}><b>Agrega valor a los datos!</b></p>
                    <Title level={5} style={{marginTop:'-10px', color:'white'}} ><b>¿Cómo lo hacemos?</b></Title>
                    <ul style={{marginTop:'-10px', marginLeft:'-30px', marginBottom:'10px'}}>
                        <li style={{color:'#CBCE07'}}>Por medio de nuestro software calculamos la huella de agua de tu proceso o producto.</li>
                    </ul>
                </Card>
            </Col>
            
            <Col xl={8} xs={24} style={{position:'absolute', marginTop: window.innerWidth>1000? '400px':'350px', marginRight:'420px'}}>
                <img src={R2} width={'250px'} />
            </Col>
            <Col xl={8} xs={24} md={1} style={{padding:'0px', position:'absolute', marginTop:window.innerWidth>1000? '400px':'350px', marginRight:window.innerWidth>1000? '1020px':'800px'}}>
                <img src={R3} width={'200px'} />
                <Title level={3} style={{position:'absolute', marginTop:'-20px', marginLeft:'55px'}}>PATNERS</Title>
            </Col>
            <Col xl={{span:16, offset:3}} xs={{span:18}} md={{span:16, offset:8}} style={{marginTop:window.innerWidth>800&window.innerWidth<1000? '40px':window.innerWidth<800?'10px':'40px'}}>
                {window.innerWidth < 800 && <h2>PATNERS</h2>}
                {window.innerWidth > 800 ? <Col>
                <img src={P1} width='60px' style={{marginRight:'30px'}} />
                <img src={P2} width='100px' style={{marginRight:'30px'}} />
                <img src={P3} width='100px' style={{marginRight:'30px'}} />
                <img src={P4} width='100px' style={{marginRight:'30px'}} />
                <img src={P5} width='100px' style={{marginRight:'30px'}} />
                </Col>:<>
                <Col span={24} style={{marginBottom:'40px', marginBottom:'20px'}} >
                    <img src={P1} width='60px' style={{marginRight:'60px'}} />
                    <img src={P2} width='100px' />
                </Col>

                <Col span={24} style={{marginBottom:'40px'}}>
                    <img src={P3} width='100px' style={{marginRight:'60px'}} />
                    <img src={P4} width='100px' />
                </Col>
                <img src={P5} width='100px' style={{marginRight:'60px'}} />
                </>}
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
        width: '100%',        
        backgroundColor: 'black',
        color: 'white',        
        borderRadius:' 0px 0px 20px 20px'
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
        padding:'20px'
    },
    row: {
        paddingTop:'90px',
        marginBottom: '0px',
        marginTop:'-90px'
    },
    titleCol: {
        backgroundColor:'#CBCE07',
        paddingLeft: window.innerWidth > 800 ? '100px':'20px',
        paddingTop:'10px',
        paddingBottom:'0px'
        
    }
}


export default Services
