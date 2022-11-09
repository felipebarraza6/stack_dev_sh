import React from 'react'
import { Row, Col, Typography, Carousel } from 'antd'
import logo_corfo from '../assets/images/corfo.png'
import logo_cidere from '../assets/images/cidere.png'

import diteco from '../assets/images/clientes/diteco.png'
import polykarpo from '../assets/images/clientes/polykarpo.png'
import placilla from '../assets/images/placilla.jpeg'
import cannes from '../assets/images/canner.png'

import im1 from '../assets/images/team/1.jpg'
import im2 from '../assets/images/team/2.jpg'

import c1 from '../assets/images/clientes/1.png'
import c2 from '../assets/images/clientes/2.png'
import c3 from '../assets/images/clientes/3.png'
import c4 from '../assets/images/clientes/4.png'
import c5 from '../assets/images/clientes/5.png'


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
      <Row justify='center'>
            <Col span={24} style={{paddingTop:'30px'}}><center>
              <img src={c1} style={{marginRight:'50px'}} width='15%' alt='logo_cowork' />
              <img src={c2} style={{marginRight:'50px'}} width='15%' alt='logo_cowork' />
              <img src={c3} style={{marginRight:'50px'}} width='15%' alt='logo_cowork' />
              <img src={c4} style={{marginRight:'50px'}} width='15%' alt='logo_cowork' />
              <img src={c5} style={{marginRight:'50px'}} width='15%' alt='logo_cowork' />
              </center>
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
        marginTop:'20px', marginBottom:'20px'   
    }
}


export default Collaborators
