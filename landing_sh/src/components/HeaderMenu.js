import React from 'react'
import {Col, Row, Button } from 'antd'
import { HashLink as Link } from 'react-router-hash-link'
import { UserOutlined } from '@ant-design/icons'


const HeaderMenu = () => {

    const pathname = window.location.pathname

    const goDataIot = () => {
        window.open('https://dataiot.smarthydro.cl')
    }


    return(
        <Row justify='start' style={styles.container}>         
            <Col xl={3} lg={6} md={4}>
                {pathname !== '/' ?                 
                    <Link smooth to="/" onClick={()=>window.location.assign('/')} style={styles.btn}>
                        MISIÓN Y VISIÓN
                    </Link>:                
                    <Link smooth to="#" style={styles.btn}>
                        MISIÓN Y VISIÓN
                    </Link>
                }
            </Col>
            <Col xl={3} lg={4} md={4}>
                {pathname !== '/' ? 
                    <Link smooth to="/" style={styles.btn} onClick={()=>window.location.assign('/')}>QUÉ HACEMOS</Link>:                
                    <Link smooth to="#about" style={styles.btn}>QUÉ HACEMOS</Link>                
                }

            </Col>
            <Col xl={3} lg={4} md={6}>
                {pathname !== '/' ? 
                    <Link smooth to="/" style={styles.btn} onClick={()=>window.location.assign('/')}>PATNERS/CLIENTES</Link>:                
                    <Link smooth to="#features" style={styles.btn}>PATNERS / CLIENTES</Link>                
                }

            </Col>                                    
            <Col xl={{span:1,offset:12}} md={{span:1,offset:5}} lg={{span:1,offset:8}}>
                <Button style={styles.btnAction} icon={<UserOutlined style={styles.usericon} />} onClick={goDataIot}>
                    <b>ACCESO DATAIOT</b>
                </Button>
            </Col>
        </Row>
    )
}


const styles = {    
    container: {
        paddingTop: '10px',        
        zIndex:100000

    },
    btn: {
        color:'black'
    },
    btnAction: {
        backgroundColor:'#222221',
        borderRadius:'10px',
        borderColor:'#222221',
        color:'white'        
    },
    usericon: {
        marginRight:'8px',
        fontSize:'20px'
    }
}


export default HeaderMenu
