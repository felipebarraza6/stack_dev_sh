
import React, { useContext, useState} from "react"

import logo_src from '../../assets/img/logo-white.png'
import 'antd/dist/antd.css'
import { Row, Col, Typography, 
        Form, Input, Button,
        notification } from 'antd'
import {AuthContext} from '../../App'
import api_crm from '../../api_crm/endpoints'

const { Title, Text } = Typography

const Pages = () => {
  
  const {dispatch} = useContext(AuthContext)

  const initialState = {
    email: '',
    password: '',
    isSubmitting: false,
    error: null
  }
  
  const [state, setState] = useState(initialState)

  const onFinish = async() => {
    try {
      const request = await api_crm.authenticated(state)      
      dispatch({
        type: 'LOGIN',
        payload: request
      })
      return request
    } catch(error) {
      notification.error({message: 'contraseña incorrecta'})
    }
  }

  const handleInputChange = e => {
    setState({
        ...state,
        [e.target.name]: e.target.value
    })
}

  const [form] = Form.useForm()

  return (
    <>      
        <div style={{backgroundColor:'#002766', height: '1000px' }}>
          <Row justify="center">            
            <Col style={styles.col} span={24}>
              <img src={logo_src} alt='logo' width='300px' />
            </Col>
            <Col>
              <Title style={styles.title}>Central de Monitoreo</Title>
              <Form onFinish={onFinish} form={form} layout='vertical' name='form_login'>
                <Form.Item name='user' label={<Text style={styles.label}>Usuario</Text>} >
                  <Input placeholder='Usuario' name='email' onChange={handleInputChange} />
                </Form.Item>
                <Form.Item name='password' label={<Text style={styles.label}>Contraseña</Text>} >
                  <Input type='password' name='password' placeholder='Contraseña' onChange={handleInputChange} />
                </Form.Item>
                <Form.Item>
                  <Button htmlType='submit' type='primary' size='large' style={styles.btn}>Ingresar</Button>
                  <Button type='primary' onClick={()=>form.resetFields()} danger size='large' style={styles.btn}>Limpiar</Button>
                </Form.Item>
              </Form>
            </Col>
          </Row>                              
        </div>      
    </>
  )
}


const styles = {
    container: {
        margin: '30px',        
    }, 
    title: {
      color: 'white',
      textAlign: 'center'
    },
    col : {
      marginTop: '10%',
      textAlign: 'center',
      marginBottom: '1%'
    },
    btn: {
      marginRight: '20px'
    },
    label: {
      color: 'white',
    }
}

export default Pages
