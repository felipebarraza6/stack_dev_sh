import React from 'react'
import { Row, Col, Steps,
        Typography, List } from 'antd'

import { TagFilled } from '@ant-design/icons'
import mapa from './../assets/images/mapa.png'

const { Step } = Steps
const { Text, Title } = Typography


const Itinerary = () => {


    return (<Row>
        <Typography.Title level={1} style={styles.title}>Presencia en Nuestra Región</Typography.Title>
        <img src={mapa} width={'100%'} />
    </Row>)
}


const styles = {
    step: {
        color: 'white'
    },
    title: {
        color: 'white',
        marginLeft:'55px',
        marginTop:'55px',
      marginBottom: '-70px'
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
