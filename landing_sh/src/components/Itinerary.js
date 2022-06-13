import React from 'react'
import { Row, Col, Steps,
        Typography, List } from 'antd'

import { TagFilled } from '@ant-design/icons'
import mapa from './../assets/images/mapa.png'

const { Step } = Steps
const { Text, Title } = Typography


const Itinerary = () => {


    return (<Row>
        <img src={mapa} width={'100%'} />
    </Row>)
}


const styles = {
    step: {
        color: 'white'
    },
    title: {
        color: 'white'
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
