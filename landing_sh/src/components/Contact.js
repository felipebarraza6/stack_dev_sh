import React from 'react'
import { Row, Col, Typography, Statistic, Card } from 'antd'
import Itinerary from './Itinerary'
import { PlusOutlined } from '@ant-design/icons'
import FormSuscription from './FormSuscription'
import cover from '../assets/images/map.png'
import mapa2 from '../assets/images/mapa2.png'
import { CircularProgressbar,buildStyles } from 'react-circular-progressbar'
import 'react-circular-progressbar/dist/styles.css'

const { Title } = Typography

const Contact = () => {

    

    return(
        <Row style={styles.container} align={'middle'}>            
            <Col xl={10} xs={24} md={12} style={{marginTop:'50px', backgroundPositionY:'center', backgroundPositionX:'center', backgroundImage: `url(${mapa2})`, backgroundSize:window.innerWidth>800?'400px ':'300px', height:'100vh', backgroundRepeat:'no-repeat'}} >
                
            </Col>
            <Col xl={14} xs={24} md={12} style={{paddingBottom:window.innerWidth<800&&'30px'}}>
                <Row align={'middle'} justify='center' >
                    <Col span={24}>
                        <Title level={1} style={{textAlign:window.innerWidth<800&&'center', color:'white', marginBottom:'30px', paddingLeft:window.innerWidth>800&&'40px'}}>Alcance en nuestro país</Title>
                    </Col>
                    <Col span={4} style={{marginBottom:'20px'}}>
                    <CircularProgressbar
                    value={70}
                    text={`50+`}
                    styles={buildStyles({
                        // Rotation of path and trail, in number of turns (0-1)
                        rotation: 0.25,

                        // Whether to use rounded or flat corners on the ends - can use 'butt' or 'round'
                        strokeLinecap: 'butt',

                        // Text size
                        textSize: '30px',

                        // How long animation takes to go from one percentage to another, in seconds
                        pathTransitionDuration: 0.5,

                        // Can specify path transition in more detail, or remove it entirely
                        // pathTransition: 'none',

                        // Colors
                        pathColor: `white`,
                        textColor: 'white',
                        trailColor: 'rgba(255, 255, 255, 0.1)',
                        backgroundColor: '#3e98c7',
                    })}
                    />
                    </Col>
                    <Col span={18}>
                        <Title level={3} style={{color:'white', marginTop:'0px', marginLeft:'20px'}}>Empresas y Organizaciones</Title>
                    </Col>
                    <Col span={4} style={{marginBottom:'20px'}}>
                    <CircularProgressbar
                    value={120}
                    maxValue={300}
                    text={`120+`}
                    styles={buildStyles({
                        // Rotation of path and trail, in number of turns (0-1)
                        rotation: 0.25,

                        // Whether to use rounded or flat corners on the ends - can use 'butt' or 'round'
                        strokeLinecap: 'butt',

                        // Text size
                        textSize: '30px',

                        // How long animation takes to go from one percentage to another, in seconds
                        pathTransitionDuration: 0.5,

                        // Can specify path transition in more detail, or remove it entirely
                        // pathTransition: 'none',

                        // Colors
                        pathColor: `white`,
                        textColor: 'white',
                        trailColor: 'rgba(255, 255, 255, 0.1)',
                        backgroundColor: '#3e98c7',
                    })}
                    />
                    </Col>
                    <Col span={18}>
                        <Title level={3} style={{color:'white', marginTop:'0px', marginLeft:'20px'}}>Sistemas de monitoreo instalados</Title>
                    </Col>
                    <Col span={4} style={{marginBottom:'20px'}}>
                    <CircularProgressbar
                    value={6000}
                    text={`7.200+`}
                    maxValue={12000}
                    styles={buildStyles({
                        // Rotation of path and trail, in number of turns (0-1)
                        rotation: 0.35,

                        // Whether to use rounded or flat corners on the ends - can use 'butt' or 'round'
                        strokeLinecap: 'butt',

                        // Text size
                        textSize: '20px',

                        // How long animation takes to go from one percentage to another, in seconds
                        pathTransitionDuration: 0.5,

                        // Can specify path transition in more detail, or remove it entirely
                        // pathTransition: 'none',

                        // Colors
                        pathColor: `white`,
                        textColor: 'white',
                        trailColor: 'rgba(255, 255, 255, 0.1)',
                        backgroundColor: '#3e98c7',
                    })}
                    />
                    </Col>
                    <Col span={18}>
                        <Title level={3} style={{color:'white', marginTop:'0px', marginLeft:'20px'}}>Agua monitoreada en tiempo real</Title>
                        <Title level={5} style={{color:'white', marginLeft:'20px',marginTop:'-15px', color:'rgba(255, 255, 255, 0.6)'}}>(litros por segundo)</Title>
                    </Col>                    
                </Row>
            </Col>
        </Row>
    )
}


const styles = {
    col: {
        paddingLeft: '5px', paddingRight:'5px'
    },
    btn: {
        marginRight:'10px',
        borderRadius: '5px'
    },
    form : {
        color:'white', 
        paddingLeft:'50px', 
        paddingRight:'50px',
        paddingTop:'30px'
    },
    container: {
        backgroundImage: `url(${cover})`,        
        paddingTop: '5px',
        paddingBottom:'5px'
    },
    title: {
        color:'white',
        textAlign: 'center'
    }, 
    text: {
        color: 'white',
    },
    label: {
        color: 'white'
    }
}


export default Contact
