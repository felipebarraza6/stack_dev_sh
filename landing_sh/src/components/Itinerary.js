import React from 'react'
import { Row, Col, Steps,
        Typography, List } from 'antd'

import { TagFilled } from '@ant-design/icons'
import mapa from './../assets/images/mapa.png'
import mapa2 from '../assets/images/mapa2.png'
const { Step } = Steps
const { Text, Title } = Typography


const Itinerary = () => {


    return (<Row justify={'center'}>
        <center><Typography.Title level={2} style={styles.title}>Alcance en el País</Typography.Title></center>
        <center><img src={mapa2} style={{marginTop: window.innerWidth > 800 ? '130px':'80px'}} width={'55%'} /></center>
    </Row>)
}


const styles = {
    step: {
        color: 'white'
    },
    title: {
        color: 'white',
        marginLeft:'55px',
        marginTop: window.innerWidth > 800 ? '55px':'-30px',
      marginBottom: '-70px',
      textAlign:'center'
    },
    title1: {
        color: 'white',
        textAlign: 'center'
    },
    containerSteps: {
        padding: '10px'
    },
    colTitle: {
        marginRight: '30px',
        marginLeft: '30px',
    }
}

export default Itinerary
