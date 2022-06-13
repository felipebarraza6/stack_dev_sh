import React from 'react'
import { Row, Col, Typography } from 'antd'
import Itinerary from './Itinerary'
import FormSuscription from './FormSuscription'

const { Title } = Typography

const Contact = () => {

    

    return(
        <Row style={styles.container} >            
            <Col xs={24} sm={24} md={12} style={{marginTop:'-50px'}} lg={12} xl={12}>
                <Itinerary />
            </Col>
            <Col xs={24} sm={24} md={12} lg={12} xl={12}>
                <Title style={styles.title}>Contacto</Title>                
                <FormSuscription />
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
        backgroundColor: '#001529',
        padding: '30px',
        paddingTop: '70px',
        paddingBottom:'60px'
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
