import React from 'react'
import { Row, Col, Typography } from 'antd'
import logo from '../assets/images/cowork_dark.png'
import { FacebookOutlined, InstagramOutlined, TwitterOutlined } from '@ant-design/icons'
const { Paragraph, Title } = Typography

const FooterFingerprint = () => {

    return(<Row justify='center' style={{paddingTop:'50px', marginTop:'70px', marginBottom:'0px', backgroundColor:'rgb(24, 144, 255)'}}>
        <Col xs={24} sm={24} md={24} lg={24} xl={24} style={{paddingLeft:'20px', paddingRight:'20px', paddingBottom:'20px'}}>
            <Title level={2} style={{textAlign: 'center', color:'white', fontStyle:'italic'}}>
                "Innovamos para cambiar vidas."
            </Title>
        </Col>
      </Row>)
}


const styles = {
    a: {
        color:'black'
    }
}

export default FooterFingerprint
