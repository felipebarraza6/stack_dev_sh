import React from 'react'
import { Row, Col, Button, Space } from 'antd'
import wallpaper from '../assets/images/sft.png'
import logo from '../assets/images/logogreen.png'
import { Link } from "react-router-dom"

const Home = () => {

    return(<Row justify='space-evenly' align='middle'  style={{
        backgroundImage:`url(${wallpaper})`,
        minHeight: '820px',    
        /* Create the parallax 
        scrolling effect */
        backgroundAttachment: 'fixed',
        backgroundPosition: 'center',
        backgroundColor:'rgb(255,255,255,0,0.7)',
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'cover',
        paddingTop:'140px'
    }}>
            <Col span={1}  style={{marginLeft:'0px', }}>
            <Link to='/mide'>
                <Button  style={{borderRadius:'12px'}} size='large'>MIDE</Button>
            </Link>
            </Col>
            <Col span={1} >
            <Link to='/huella'>
                <Button style={{borderRadius:'12px'}} size='large'>COMPARA</Button>
            </Link>
            </Col>
            <Col span={1} >
            <Link to='/construccion'>
                <Button  style={{borderRadius:'12px'}} size='large'>REDUCE</Button>
            </Link>
            </Col> 
            <Col span={1} >
            <Link to='/construccion'>
                <Button  style={{borderRadius:'12px'}} size='large'>COMPENSA</Button>
            </Link>
        </Col>        
        
    </Row>)
}


export default Home
