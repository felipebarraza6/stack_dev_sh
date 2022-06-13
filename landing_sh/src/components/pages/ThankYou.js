import React from 'react'
import {Row, Col, Typography, Card} from 'antd'

const ThankYou = () => {

  return(<Row justify="center" style={{paddingBottom:'250px', paddingTop:'100px', backgroundColor:'rgb(0, 21, 41)', width:'100%'}}>
    <Col>
      <Card>
        <Typography.Title level={2}>Gracias</Typography.Title>
        <Typography.Paragraph>
          Por contactarnos nos pondremos en contacto a la brevedad, que tenga buen día.   
        </Typography.Paragraph>
        <Typography.Paragraph>Smart Hydro.</Typography.Paragraph> 
      </Card>
    </Col>
  </Row>)

}


export default ThankYou
