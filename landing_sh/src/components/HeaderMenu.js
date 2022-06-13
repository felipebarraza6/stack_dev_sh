import React from 'react'
import {Col, Row } from 'antd'
import { HashLink as Link } from 'react-router-hash-link'

const HeaderMenu = ({ is_mobile }) => {

  const pathname = window.location.pathname

    return(
        <Row >         
            <Col style={styles.col}>
                {pathname !== '/' ? 
                <Link smooth to="/" onClick={()=>window.location.assign('/')} style={styles.btn}>INICIO</Link>:                
                <Link smooth to="#" style={styles.btn}>INICIO</Link>                
                }
            </Col>
            <Col style={styles.col}>
                {pathname !== '/' ? 
                <Link smooth to="/" style={styles.btn} onClick={()=>window.location.assign('/')}>MISIÓN Y VISIÓN</Link>:                
                <Link smooth to="#about" style={styles.btn}>MISIÓN Y VISIÓN</Link>                
                }

            </Col>
            <Col style={styles.col}>
                {pathname !== '/' ? 
                <Link smooth to="/" style={styles.btn} onClick={()=>window.location.assign('/')}>QUÉ HACEMOS</Link>:                
                <Link smooth to="#features" style={styles.btn}>QUÉ HACEMOS</Link>                
                }

            </Col>                        
            <Col style={styles.col}>
                {pathname !== '/' ? 
                <Link smooth to="/" onClick={()=>window.location.assign('/')} style={styles.btn}>PATNERS/CLIENTES</Link>:
                <Link smooth to="#colaborators" style={styles.btn}>PATNERS/CLIENTES</Link>                
                }

            </Col>
            <Col style={styles.col}>
                {pathname !== '/' ? 
                <Link smooth to="/" onClick={()=>window.location.assign('/')} style={styles.btn}>CONTACTO</Link>:
                <Link smooth to="#contact" style={styles.btn}>CONTACTO</Link>
                }
            </Col>
            <Col style={styles.col}>
                 <a style={{borderRadius:'5px',borderColor:'#1890ff',color:'#1890ff', padding:'10px',backgroundColor:'white'}} target='__blank' href='http://dataiot.smarthydro.cl'>
                  <b>ACCESO CLIENTES</b>
                </a>
            </Col>
        </Row>
    )
}


const styles = {
    col: {
        color:'white',
        marginLeft:'20px', 
        paddingRight:'20x'        
    },
    btn: {
        color:'white'
    }
}


export default HeaderMenu
