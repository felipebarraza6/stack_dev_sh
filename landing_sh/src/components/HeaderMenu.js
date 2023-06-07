import React from 'react'
import {Col, Row, Button } from 'antd'
import { HashLink as Link } from 'react-router-hash-link'
import { UserOutlined, FundOutlined } from '@ant-design/icons'
import icono_logo from '../assets/images/icono_logo.png'


const HeaderMenu = () => {

    const pathname = window.location.pathname

    const goDataIot = () => {
        window.open('https://dataiot.smarthydro.cl')
    }


    return(
        <Row justify='center' align={'middle'} style={styles.container}>         
            <Col xl={2} lg={6} md={4}>
                <img src={icono_logo} width={'50px'} />
            </Col>
            <Col xl={3} lg={6} md={4}>
                {pathname !== '/' ?                 
                    <Link smooth to="/" onClick={()=>window.location.assign('/')} style={styles.btn}>
                        <b>MISIÓN Y VISIÓN</b>
                    </Link>:                
                    <Link smooth to="#about" style={styles.btn}>
                        <b>MISIÓN Y VISIÓN</b>
                    </Link>
                }
            </Col>
            <Col xl={3} lg={4} md={4}>
                {pathname !== '/' ? 
                    <Link smooth to="/" style={styles.btn} onClick={()=>window.location.assign('/')}><b>QUÉ HACEMOS</b></Link>:                
                    <Link smooth to="#features" style={styles.btn}><b>QUÉ HACEMOS</b></Link>                
                }

            </Col>
            <Col xl={3} lg={4} md={6}>
                {pathname !== '/' ? 
                    <Link smooth to="/" style={styles.btn} onClick={()=>window.location.assign('/')}><b>PATNERS/CLIENTES</b></Link>:                
                    <Link smooth to="#colaborators" style={styles.btn}><b>PATNERS / CLIENTES</b></Link>                
                }

            </Col>                                    
            <Col xl={{span:1,offset:0}} md={{span:1,offset:0}} lg={{span:1,offset:0}} style={{paddingLeft:'10px'}}>
                <Button size='large' style={styles.btnAction} icon={<FundOutlined style={styles.usericon} />} onClick={goDataIot}>
                    <b>IKOLU APP</b>
                </Button>
            </Col>
        </Row>
    )
}


const styles = {    
    container: {
        paddingBottom:'10px',
        
        zIndex:100000

    },
    btn: {
        color:'black'
    },
    btnAction: {
        backgroundColor:'#222221',
        borderRadius:'10px',
        borderColor:'#222221',
        color:'white',
        
    },
    usericon: {
        marginRight:'8px',        
        fontSize:'20px',
    }
}


export default HeaderMenu
