import React from 'react'
import { Row, Col, Input, Button, Space } from 'antd'
import wallpaper from '../assets/images/wallpaper.png'
import { Link } from "react-router-dom"
import logo from '../assets/images/logozivo.png'

const Login = () => {
    return(<Row align={'middle'} justify='center' style={{
        backgroundImage:`url(${wallpaper})`,
        minHeight: '720px',    
      /* Create the parallax 
      scrolling effect */
      backgroundAttachment: 'fixed',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      backgroundSize: 'cover'

    
    }} >
        <Col offset={12} span={12} style={{paddingLeft:'130px', paddingRight:'40px', marginTop:'-130px'}}>
        <Space direction="vertical" size="middle" style={{ display: 'flex' }}>
            <center><img src={logo} width='80px' /></center>
            <Input placeholder='Usuario' style={{borderRadius:'10px'}} />
            <Input placeholder='Contraseña' style={{borderRadius:'10px'}} />
            <Link to='/inicio'><Button block style={{borderRadius:'10px'}}>Ingresar</Button></Link>
            </Space>
        </Col>

    </Row>)
}


export default Login