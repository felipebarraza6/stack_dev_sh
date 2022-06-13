import React, { useState } from 'react'
import Slide1 from '../assets/images/slide1.png'
import Slide2 from '../assets/images/slide2.png'
import Slide3 from '../assets/images/slide3.png'

import FormSuscription from './FormSuscription'

import { Card, Row, Col, 
        Typography, Affix, Button, Carousel } from 'antd'

import { CloseCircleOutlined } from '@ant-design/icons'

const { Title, Paragraph } =  Typography


const Sliders = ({is_mobile}) => {

    const [viewForm, setViewForm] = useState(true)

    return(<>
              <Carousel autoplay={true} dots={true} >
                
                <div>
              
                  <img width={'100%'} src={Slide1} />

                </div>
                <div>
                  <a href='https://smarthydro.cl/contacto'>
                  <img width={'100%'} src={Slide2} />
                  </a>
                </div>
                <div>
                  
                  <a href='https://smarthydro.cl/contacto'>
                  <img width={'100%'} src={Slide3} />
                  </a>
                </div>

              </Carousel>
                
            </>                    
    )

}


const styles = {
    title: {
        color: 'white',
    },
    col: {
        paddingTop:'0px'
    },
    card: {
        width: '700px',
        backgroundColor: '#1890ff',
        borderColor: '#1890ff',
        borderRadius: '20px',
        color: 'white',
        marginTop: '10px',
        zIndex: '1'
    },
    card2: {
        width: '100% auto',
        backgroundColor: '#1890ff',
        borderColor: '#1890ff',
        borderRadius: '20px',
        color: 'white',
        marginTop:'10px',
        zIndex: '1'
    },
    slide: {
        width: '100%',
        position: 'relative',
    },
    close: {
        color: 'white',
        fontSize: '25px'        
    }
}


export default Sliders
