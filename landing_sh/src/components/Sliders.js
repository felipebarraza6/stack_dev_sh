import React from 'react'
import Slide from '../assets/images/slide/1.png'
import Logo from '../assets/images/logo2.png'
import Yellow from '../assets/images/elements/yellow.png'
import { FacebookOutlined, InstagramOutlined, TwitterOutlined, LinkedinOutlined, WhatsAppOutlined } from '@ant-design/icons'
import FormSuscription from './FormSuscription'

import { Card, Row, Col, 
        Typography, Affix, Button, Carousel } from 'antd'


const { Title, Paragraph } =  Typography


const Sliders = ({is_mobile}) => {
    

    return(<Row style={styles.container} align="middle" justify={'center'}>
      <Col style={styles.col} xl={16} lg={16} md={24} xs={24}>
        <img src={Logo} style={styles.logo} />
        <Title style={styles.title} level={window.innerWidth>800?1:2}>INNOVAMOS PARA CAMBIAR VIDAS</Title>
        <Title level={window.innerWidth>800?3:4} style={styles.title3}>
          Buscamos el consumo sostenible del recurso hídrico mediante la implementación de tecnologías de impacto.
        </Title>
      </Col>    
      <Col span={12} style={styles.elementYellow}>
        <img src={Yellow} style={styles.elementYellow} />
      </Col>
      <Col xl={{span:1, offset:23}} xs={{span:16, offset:3}} md={{span:1,offset:22}}  style={{marginTop:window.innerWidth>1000?'-550px':window.innerWidth<800?'0px':'-750px', borderRadius:'10px'}}>
        <a href='https://www.facebook.com/smarthydrorrss/' target={'__blank'}>
          <FacebookOutlined style={{fontSize:'30px', margin:'5px', color:'black', backgroundColor:'rgb(203, 206, 7)', padding:'5px',borderRadius:'10px'}} />
        </a>
        <a href='https://www.instagram.com/smarthydrorrss/' target={'__blank'}>
          <InstagramOutlined style={{fontSize:'30px', margin:'5px', color:'black', backgroundColor:'rgb(203, 206, 7)', padding:'5px',borderRadius:'10px'}} />
        </a>
        <a href='https://twitter.com/smarthydrorrss' target={'__blank'}>
          <TwitterOutlined style={{fontSize:'30px', margin:'5px', color:'black', backgroundColor:'rgb(203, 206, 7)', padding:'5px',borderRadius:'10px'}} />
        </a>
        <a href='#' target={'__blank'}>
          <LinkedinOutlined style={{fontSize:'30px', margin:'5px', color:'black', backgroundColor:'rgb(203, 206, 7)', padding:'5px',borderRadius:'10px'}} />
          </a>
        <a href='https://web.whatsapp.com/send?phone=56939581688&text=%C2%A1Hola!' target={'__blank'}>
          <WhatsAppOutlined style={{fontSize:'30px', margin:'5px', color:'black', backgroundColor:'rgb(203, 206, 7)', padding:'5px',borderRadius:'10px'}} />
        </a>
      </Col>                                  
      
    </Row>)

}


const styles = {
  elementYellow: {
    position:'absolute',
    width: window.innerWidth > 800 ? '50%':'80%',
    marginLeft: window.innerWidth > 1000 ? '-270px': window.innerWidth > 800 ? '-180px':'-80px',
    marginTop: '-120px'
  },  
  title: {
    color: 'white',
    marginTop:'-10px',
    marginLeft: '100px'
  },
  title3: {
    color: 'white',
    marginTop: window.innerWidth > 800 ? '-20px':'10px',
    marginLeft: '100px'    
  },
  col: {    
    paddingLeft:window.innerWidth>800?'170px':'50px',
    paddingTop:window.innerWidth>800?'120px':'50px'
  },
  col2:{    
    
  },
  logo:{
    width: window.innerWidth > 800 ? '400px':'300px'
  },
  container: {    
      /* The image used */
      backgroundImage:`url(${Slide})`,
      /* Set a specific height */
      minHeight: '600px',    
      /* Create the parallax 
      scrolling effect */
      backgroundAttachment: 'fixed',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      backgroundSize: 'cover'
  }        
}


export default Sliders
