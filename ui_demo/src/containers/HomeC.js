import React from 'react'
import { Row, Col, Button, Space, Typography } from 'antd'
import wallpaper from '../assets/images/wallpaper2.png'
import logo from '../assets/images/logogreen.png'
import { Link } from "react-router-dom"

const HomeC = () => {

    return(<Row align='middle' justify='center' style={{
        backgroundImage:`url(${wallpaper})`,
        minHeight: '820px',    
        /* Create the parallax 
        scrolling effect */
        backgroundAttachment: 'fixed',
        backgroundPosition: 'center',
        backgroundColor:'rgb(255,255,255,0,0.7)',
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'cover'
    }}>
        <Col>
            <img src={logo} width='80px' />
        </Col>
        <Col span={24} style={{marginTop:'-450px', paddingLeft:'230px', paddingRight:'230px'}}>
        <Space direction="vertical" size="middle" style={{ display: 'flex' }}>
            <center>
            <Typography.Title style={{color:'white'}}>Modulo en construcción...</Typography.Title>
            </center>
            <Link to='/'>
                <Button block style={{borderRadius:'12px'}} size='large'>Volver al inicio</Button>
            </Link>
        </Space>
        </Col>        
        
    </Row>)
}


export default HomeC
