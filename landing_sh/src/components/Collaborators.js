import React from 'react'
import { Row, Col, Typography, Carousel } from 'antd'


import im1 from '../assets/images/team/1.jpg'
import im2 from '../assets/images/team/2.jpg'

import c1 from '../assets/images/clientes/1.png'
import c2 from '../assets/images/clientes/2.png'
import c3 from '../assets/images/clientes/3.png'
import c4 from '../assets/images/clientes/4.png'
import c5 from '../assets/images/clientes/5.png'
import c6 from '../assets/images/clientes/6.png'
import c7 from '../assets/images/clientes/7.png'
import c8 from '../assets/images/clientes/8.png'
import c9 from '../assets/images/clientes/9.png'
import c10 from '../assets/images/clientes/10.png'
import c11 from '../assets/images/clientes/11.png'
import c12 from '../assets/images/clientes/12.png'
import c13 from '../assets/images/clientes/13.png'


const { Title } = Typography

const Collaborators = () => {

    return (<>        
        <Carousel autoplay dotPosition='right'>
              <div>
                <img src={im1} 
                  style={{
                    width:'100%',
                    height: '500px',
                    objectFit: 'cover'
                  }} />
                  
              </div>
              <div>
                <img src={im2} 
                  style={{
                    width:'100%',
                    height: '500px',
                    objectFit: 'cover'
                  }} />
                  
              </div>
                
        </Carousel>
      <Row style={{marginTop:'-100px'}} justify='center'>
        <Col style={{backgroundColor:'white', paddingLeft:'40px', paddingRight:'40px', borderRadius:'300px 300px 0px 0px', paddingTop:'0px'}}>
        <Title level={1} style={styles.title}>Clientes</Title>
        </Col>
      </Row>
      <Row>
        <Col span={24} style={{marginBottom:'-30px'}} >
      <Carousel autoplay >
        <div>
          <Row justify={'space-around'} align={'middle'} style={{paddingTop:'20px'}}>
            <Col span={4}>
            <img src={c1}  width='100%' alt='logo_cowork' />
            </Col>
            <Col span={4}>
            <img src={c2} width='100%' alt='logo_cowork' />
            </Col>
            <Col span={4}>
            <img src={c3} width='100%' alt='logo_cowork' />
            </Col>
            <Col span={4}>
            <img src={c4} width='100%' alt='logo_cowork' />
            </Col>
            <Col span={4}>
            <img src={c5} width='100%' alt='logo_cowork' />
            </Col>
          </Row>
        </div>
        <div>
          <Row justify={'space-around'} align={'middle'}>
            <Col span={4}>
            <img src={c6}  width='100%' alt='logo_cowork' />
            </Col>
            <Col span={4}>
            <img src={c7} width='100%' alt='logo_cowork' />
            </Col>
            <Col span={4}>
            <img src={c8} width='100%' alt='logo_cowork' />
            </Col>
            <Col span={4}>
            <img src={c9} width='100%' alt='logo_cowork' />
            </Col>
            <Col span={4}>
            <img src={c10} width='100%' alt='logo_cowork' />
            </Col>
          </Row>
        </div>
        <div>
          <Row justify={'space-around'} align={'middle'}>
            <Col span={4}>
            <img src={c11}  width='70%' alt='logo_cowork' />
            </Col>
            <Col span={4}>
            <img src={c12} width='70%' alt='logo_cowork' />
            </Col>
            <Col span={4}>
            <img src={c13} width='70%' alt='logo_cowork' />
            </Col>            
          </Row>
        </div>
      </Carousel>
      </Col>
      </Row>
    </>)

}


const styles = {
    container: {
        marginTop: '15px',
        marginBottom: '40px'        
    },
    colTitle: {
        marginBottom:'3px'
    },
    logo: {
        width: '200px'
    },
    logo_mentorinn: {
        width: '300px'
    },
    logo_cowork: {
        width: '300px',        
        marginTop: '-20px'
    },
    logo_cidere: {
        width: '140px',
    },
    logo_cdn: {
        width: '300px',
        
    },
    title: {
        textAlign: 'center',
        marginTop:'40px',
        marginBottom: '20px'
    },
    colImg: {
        textAlign: 'center',
        
    }
}


export default Collaborators
