import React from 'react'
import { Row, Col, Typography } from 'antd'
import logo from '../assets/images/cowork_dark.png'
import { FacebookOutlined, InstagramOutlined, TwitterOutlined } from '@ant-design/icons'
const { Paragraph, Title } = Typography

const FooterInfo = () => {

    return(<Row justify='center' style={{marginTop:'70px', marginBottom:'70px'}}>
        <Col xs={24} sm={12} md={6} lg={6} xl={6} style={{paddingLeft:'20px', paddingRight:'20px', paddingBottom:'20px'}}>
            <Title level={2} style={{textAlign: 'center'}}>
                Innovamos para cambiar vidas.
            </Title>
        </Col>
        <Col xs={24} sm={12} md={6} lg={6} xl={6} style={{paddingLeft:'20px',paddingRight:'20px', paddingBottom:'20px'}}>
            <Title level={4} style={{marginBottom: '20px', textAlign: 'center'}}>Redes Sociales</Title>
            <Row>
                <Col span={8} style={{textAlign: 'center'}}>                    
                    <a href='https://www.facebook.com/smarthydrorrss/' noreferrer={true} target='__blank'>
                        <FacebookOutlined style={{fontSize:'30px', color: '#3b5998'}} />
                    </a>                    
                </Col>
                <Col span={8} style={{textAlign: 'center'}}>                    
                    <a noreferrer={true} href='https://www.instagram.com/smarthydrorrss/' target='__blank'>
                        <InstagramOutlined style={{fontSize:'30px', color: '#3f729b'}} />
                    </a>
                </Col>
                <Col span={8} style={{textAlign: 'center'}}>                    
                    <a href='https://twitter.com/smarthydrorrss' noreferrer={true} > 
                        <TwitterOutlined style={{fontSize:'30px', color: '#00acee'}} />
                    </a>
                </Col>
            </Row>
        </Col>
        <Col xs={24} sm={12} md={6} lg={6} xl={6} style={{paddingLeft:'20px', paddingRight:'20px', paddingBottom:'20px'}}>
            <Title level={4} style={{marginBottom: '20px', textAlign: 'center', textAlign:'center'}}>Contacto</Title>
            <Paragraph align="center">
                <a style={styles.a} href='tel:56939581688' target='_blank' rel='noreferrer'>+56 9 39581688</a>
            </Paragraph>
            <Paragraph align="center">
                <a style={styles.a} href='mailto:contacto@smarthydro.cl' target='_blank' rel='noreferrer'>contacto@smarthydro.cl</a>
            </Paragraph>
        </Col>
        <Col xs={24} sm={12} md={6} lg={6} xl={6} >
      <center>
            <a style={styles.a} href='#' target='_blank' rel='noreferrer'>
                <img src={logo} alt='logo' width='200px'/>
            </a></center>
        </Col>
    </Row>)
}


const styles = {
    a: {
        color:'black'
    }
}

export default FooterInfo
