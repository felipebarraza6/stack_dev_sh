import React, { useState, useEffect } from 'react'
import HeaderMenu from '../components/HeaderMenu'
import { Layout, Col, Row, 
          Typography, Button } from 'antd'
import logo_src from '../assets/images/logo.png'
import logo_src2 from '../assets/images/logo2.png'
import icono_logo from '../assets/images/icono_logo.png'
import Sliders from '../components/Sliders'
import About from '../components/About'
import Services from '../components/Services'
import Contact from '../components/Contact'
import Collaborators from '../components/Collaborators'
import FooterInfo from '../components/FooterInfo'
import InternalLifting from '../components/pages/InternalLifting'
import FooterFingerprint from '../components/FooterFingerprint'
import { BrowserRouter, Redirect, Route } from 'react-router-dom'
import ContainerFormDga from '../components/dgaform/ContainerFormDga'
import ContactForm from '../components/forms/ContactForm'
import Fingerprint from '../components/fingerprint/Init'
import { FundOutlined } from '@ant-design/icons'
import ThankYou from '../components/pages/ThankYou'
import WebinarRetrieve from '../components/webinars/webinarRetrieve'
import QuotationExternalClients from './Quotation'
import QuotationDefine from './QuotationDefine'
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

    const goDataIot = () => {
      window.open('https://dataiot.smarthydro.cl')
  }

    var event = new Date()
    var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }

    return(<Layout style={styles.layout}>
        <BrowserRouter>                            
              <Route exact path='/'>                
                <Header style={styles.header} >            
                  <Row align='middle' justify={'center'}>
                    {width > 800 ? <>
                       
                      <Col span={22}> 
                        <HeaderMenu is_mobile={is_mobile} />
                      </Col>                
                    </>:<>
                      <Col style={styles.colLogoMobil} span={12}>
                        <a href='https://smarthydro.cl'>
                        <img src={icono_logo} alt='logo' style={styles.logo} />
                        </a>
                      </Col>
                      <Col span={12}>
                      <Button size='large' style={styles.btnAction} icon={<FundOutlined style={styles.usericon} />} onClick={goDataIot}>
                    <b>IKOLU APP</b>
                </Button>
                      </Col>
                      </>}
                  </Row>
                </Header>                
              </Route>
              <Route exact path='/fingerprint/:id'>
              <Header style={styles.header}>            
                <Row>                
                    <Col  span={2} offset={22}>
                      <center>
                        <a href='https://smarthydro.cl'>
                          <img src={icono_logo} alt='logo' style={styles.logoh} />
                        </a>
                      </center>
                    </Col>
                </Row>
              </Header>
              </Route>
              <Content>
              <Route exact path='/fingerprint/:id' component={Fingerprint} />
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
              <Route exact path='/internal_lifting' >
                <InternalLifting />
              </Route>
              <Route exact path='/quotations/client/:id' component={QuotationExternalClients} >
              </Route>

              <Route exact path='/dgaform/external_client/:id' component={ContainerFormDga} >
              </Route>
              <Route exact path='/contacto'>
                <ContactForm />
              </Route>
              <Route exact path='/gracias'>
                <ThankYou />
              </Route>
              <Route exact path='/webinars/:id' component ={WebinarRetrieve} />
        </Content>
      <Route exact path='/'>
        <Footer style={{backgroundColor:'#1F3461'}}>
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
  btnAction: {    
    borderRadius:'10px',    
    color:'black',
    backgroundColor: 'rgb(203, 206, 7)',
    borderColor: 'rgb(203, 206, 7)',
    marginTop:'20px'
},
    layout: {
      backgroundColor: 'white'
    },
    marginCol: {
        paddingTop:'20px',
        paddingBottom: '40px'
    },

    usericon: {
      marginRight:'8px',
      fontSize:'20px'
  },
    logo: {
        width: window.innerWidth<800?'35px':'50px',                
    },
    logoh: {
      width: '55px'
    },
    logo2: {
      width: '200px',
      padding:'10px'
      
    },
    colLogoMobil: {
      
    },
    title: {
        color:'white', 
        margin: '13px'
    },
    header: {
        backgroundColor: 'white',
        marginBottom:'40px',        
        paddingTop:'10px'
    },
    header1: {
        backgroundColor: '#1890ff',
        paddingBottom:  window.innerWidth > 800 ? '0px':'100px'
    }
}


export default Home
