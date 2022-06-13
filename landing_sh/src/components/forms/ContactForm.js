import React from 'react'
import { Row, Col, Typography } from 'antd'
import Contact from '../Contact'

const ContactForm = () => {

  return(<Row style={{backgroundColor: 'rgb(0, 21, 41)', color:'white', paddingTop:'50px', paddingRight:'50px'}}>
            <Col span={12}></Col>
            <Col span={12}>
              <Typography.Title level={3} style={{color:'white'}}>Déjanos tus datos y nos pondremos en contacto a la brevedad.
</Typography.Title>
            </Col>
            <Contact />
        </Row>)

}


export default ContactForm
