import React, { useState, useEffect } from 'react'
import HeaderMenu from '../components/HeaderMenu'
import { Layout, Col, Row, Typography } from 'antd'
import logo_src from '../assets/images/logo.png'
import logo_src2 from '../assets/images/logo2.png'
import Sliders from '../components/Sliders'
import About from '../components/About'
import Services from '../components/Services'
import Contact from '../components/Contact'
import Collaborators from '../components/Collaborators'
import FooterInfo from '../components/FooterInfo'
import FooterFingerprint from '../components/FooterFingerprint'
import { BrowserRouter, Redirect, Route } from 'react-router-dom'
import ContainerFormDga from '../components/dgaform/ContainerFormDga'
import ContactForm from '../components/forms/ContactForm'
import Fingerprint from '../components/fingerprint/Init'
import ThankYou from '../components/pages/ThankYou'
import WebinarRetrieve from '../components/webinars/webinarRetrieve'
import { InstagramOutlined,TwitterOutlined,FacebookOutlined, 
          WhatsAppOutlined, PhoneOutlined, MailOutlined } from '@ant-design/icons'
import QuotationExternalClients from './Quotation'
const { Header, Content, Footer } = Layout

const Home = () => {


    const [width, setWidth] = useState()
    const [is_mobile, setIsMobile] = useState()    

    useEffect(()=> {
        setWidth(window.innerWidth)
          if(window.innerWidth > 800){
            setIsMobile(true)
          }
    }, [])

    var event = new Date()
    var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }

    return(<Layout>
        <BrowserRouter>              
              <Route exact path='/'>
              <Header style={styles.header1}>
                <Row justify='end'>
                  <Col><a href='https://www.facebook.com/smarthydrorrss/' target='_blank'>
                    <FacebookOutlined style={{color:'white', fontSize:'20px', marginRight:'25px' }}/>
                  </a></Col>
                  <Col><a target='_blank' href='https://twitter.com/smarthydrorrss'>
                    <TwitterOutlined style={{color:'white', fontSize:'20px', marginRight:'25px' }}/>
                  </a></Col>
                  <Col><a target='_blank' href='https://www.instagram.com/smarthydrorrss/'>
                    <InstagramOutlined style={{color:'white', fontSize:'20px', marginRight:'25px' }}/>
                  </a></Col>
                  <Col><a target='_blank' href='https://web.whatsapp.com/send?phone=56939581688&text=¡Hola!'>
                    <WhatsAppOutlined style={{color:'white', fontSize:'20px', marginRight:'25px' }}/>
                  </a></Col>
                  <Col><a target='_blank' href='tel:56939581688'>
                    <PhoneOutlined style={{color:'white', fontSize:'20px', marginRight:'25px' }}/>
                  </a></Col>
                  <Col><a target='_blank' href='mailto:contacto@smarthydro.cl'>
                    <MailOutlined style={{color:'white', fontSize:'20px', marginRight:'25px' }}/>
                  </a></Col>
                </Row>
              </Header>
              </Route>
              <Route exact path='/fingerprint/:id'>
              <Header style={styles.header1}>
              </Header>
              </Route>
              <Route path='/quotations/'>
                <Row style={{padding:'10px', backgroundColor:'#1890ff'}} justify="start">
                  <Col span={width > 800 ? 18:24}>
                  <img src={logo_src2} alt='logo' style={styles.logo2} />                 
                  </Col>
                  <Col span={width > 800 ? 6:24}>
                    <Typography.Title level={4} style={{color:'white', paddingTop:'8%'}}> {event.toLocaleDateString('es-ES', options)} </Typography.Title>
                  </Col>
                </Row>
              </Route>
              <Route exact path='/'>
              <Header style={styles.header}>            
                <Row >                
                  {width > 800 ? <>
                    <Col span={4}>
                      <a href='https://smarthydro.cl'>
                      <img src={logo_src} alt='logo' style={styles.logo} />
                      </a>
                    </Col>
                    <Col span={5}>
                    </Col>                
                    <Col span={15}> 
                      <HeaderMenu is_mobile={is_mobile} />
                    </Col>                
                  </>: 
                    <Col style={styles.colLogoMobil} span={24}>
                      <a href='https://smarthydro.cl'>
                      <img src={logo_src} alt='logo' style={styles.logo} />
                      </a>
                    </Col>}
                </Row>
              </Header>
              </Route>
              <Route exact path='/fingerprint/:id'>
              <Header style={styles.header}>            
                <Row >                
                  {width > 800 ? <>
                    <Col span={4}>
                      <a href='https://smarthydro.cl'>
                      <img src={logo_src} alt='logo' style={styles.logo} />
                      </a>
                    </Col>
                    <Col span={5}>
                    </Col>                
                    <Col span={15}> 
                      <Row justify='end'>
                  <Col><a href='https://www.facebook.com/smarthydrorrss/' target='_blank'>
                    <FacebookOutlined style={{color:'white', fontSize:'20px', marginRight:'25px' }}/>
                  </a></Col>
                  <Col><a target='_blank' href='https://twitter.com/smarthydrorrss'>
                    <TwitterOutlined style={{color:'white', fontSize:'20px', marginRight:'25px' }}/>
                  </a></Col>
                  <Col><a target='_blank' href='https://www.instagram.com/smarthydrorrss/'>
                    <InstagramOutlined style={{color:'white', fontSize:'20px', marginRight:'25px' }}/>
                  </a></Col>
                  <Col><a target='_blank' href='https://web.whatsapp.com/send?phone=56939581688&text=¡Hola!'>
                    <WhatsAppOutlined style={{color:'white', fontSize:'20px', marginRight:'25px' }}/>
                  </a></Col>
                  <Col><a target='_blank' href='tel:56939581688'>
                    <PhoneOutlined style={{color:'white', fontSize:'20px', marginRight:'25px' }}/>
                  </a></Col>
                  <Col><a target='_blank' href='mailto:contacto@smarthydro.cl'>
                    <MailOutlined style={{color:'white', fontSize:'20px', marginRight:'25px' }}/>
                  </a></Col>
                </Row>
                    </Col>                
                  </>: 
                    <Col style={styles.colLogoMobil} span={24}>
                      <a href='https://smarthydro.cl'>
                      <img src={logo_src} alt='logo' style={styles.logo} />
                      </a>
                    </Col>}
                </Row>
              </Header>
              </Route>
        <Content>
              <Route exact path='/'> 
                <>
                  <Col span={24} >
                      <Sliders is_mobile={is_mobile} />
                  </Col>
                  <Col span={24} id='about'>
                      <About />
                  </Col>
                  <Col span={24} id='features'>
                      <Services />
                  </Col>
                  <Col span={24} id='colaborators' style={styles.marginCol}>
                      <Collaborators />
                  </Col>
                  <Col span={24} id="contact">
                      <Contact />
                  </Col> 
                </> 
              </Route>
              <Route exact path='/dgaform/new'>                
                <Redirect to='/quotations/new' />
              </Route>
              <Route exact path='/quotations/new' >
                <QuotationExternalClients />
              </Route>
              <Route exact path='/dgaform/external_client/:id' component={ContainerFormDga} >
              </Route>
              <Route exact path='/fingerprint/:id' component={Fingerprint} />
              <Route exact path='/fingerprint/root/:id' component={Fingerprint} />
              <Route exact path='/contacto'>
                <ContactForm />
              </Route>
              <Route exact path='/gracias'>
                <ThankYou />
              </Route>
              <Route exact path='/webinars/:id' component ={WebinarRetrieve} />
        </Content>
      <Route exact path='/'>
        <Footer>
            <FooterInfo />
        </Footer>
      </Route>
      <Route exact path='/dgaform/external_client/:id'>
        <Footer>
            <FooterInfo />
        </Footer>
      </Route>
      <Route exact path='/fingerprint/:id'>
        <FooterFingerprint /> 
      </Route>
        </BrowserRouter>
            </Layout>)
}


const styles = {
    marginCol: {
        paddingTop:'20px',
        paddingBottom: '40px'
    },
    logo: {
        width: '250px',
        marginTop: '-125px'
    },
    logo2: {
      width: '200px',
      padding:'10px'
      
    },
    colLogoMobil: {
        textAlign: 'center',
    },
    title: {
        color:'white', 
        margin: '13px'
    },
    header: {
        backgroundColor: '#1890ff',
    },
    header1: {
        backgroundColor: '#1890ff',
        paddingBottom:  window.innerWidth > 800 ? '0px':'100px'
    }

    
}


export default Home
