import React from 'react'
import { Row, Col, Typography, Carousel } from 'antd'
import logo_cowork from '../assets/images/parners/essbio.png'
import logo_corfo from '../assets/images/corfo.png'
import logo_mentorinn from '../assets/images/parners/biodiversa.png'
import logo_cidere from '../assets/images/cidere.png'
import logo_cdn from '../assets/images/parners/asoex.png'

import diteco from '../assets/images/clientes/diteco.png'
import polykarpo from '../assets/images/clientes/polykarpo.png'
import placilla from '../assets/images/placilla.jpeg'
import cannes from '../assets/images/canner.png'


const { Title } = Typography

const Collaborators = () => {

    return (<>
        <Row justify='center' style={{marginTop:'50px'}}>          
          <Title style={{marginBottom:'20px'}}>Patners</Title>
        </Row>
        <Carousel autoplay>
          <div>
            <Row justify='space-around'>
              <Col>
                <img src={'https://www.ubiobio.cl/mcc/images/logosimbologia.png'} 
                  width="100" alt='logo_cowork' />
              </Col>
              <Col>
                <img src={logo_corfo} 
                  width="250" alt='logo_cowork' />
              </Col>
              <Col>
                <img src={logo_cidere} 
                  width="120" alt='logo_cowork' />
              </Col>
              <Col>
              <img src={'https://veset.cl/wp-content/uploads/2022/01/LOGO-VESET-CON-%C2%AE.png'} 
                width="200" alt='logo_cowork' />
            </Col>

          </Row>
        </div>
        </Carousel>
      <Row style={{marginTop:'50px'}} justify='center'>
        <Title level={1} style={styles.title}>Clientes</Title>
      </Row>
      <Carousel autoplay style={{marginBottom:'120px'}}>
        <div>
            <Row justify='space-around'>
            <Col>
              <img src={diteco} style={styles.ditecologo_cowork} alt='logo_cowork' />
            </Col>
            <Col>                
              <img src={polykarpo} style={styles.ditecologo_cowork} alt='logo_corfo' />
            </Col>
            <Col>                
              <img width="200" src={'https://empresasiansa.cl/wp-content/uploads/2021/02/divisi%C3%B3n-industrial-02-e1613423333912.png'} alt='logo_corfo' />
            </Col>
             
          </Row>
        </div>
        <div>
          <Row justify='space-around'>
            <Col>                
              <img src={placilla} width={'150px'} alt='logo_corfo' />
            </Col>  
            <Col>                
              <img src={cannes} width={'300px'} alt='logo_corfo' />
            </Col>
          </Row>
        </div>
      </Carousel>
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
