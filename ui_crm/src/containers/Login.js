// React
import React from 'react'

// Build
import logo from '../build/images/logo-white.png'

// Antd
import { Form, Input, Button, Checkbox, Spin, message } from 'antd';

// Antd Icons
import { UserOutlined, LockOutlined } from '@ant-design/icons'

// Context
import { AuthContext } from '../App'

// Endpoints
import api  from '../api/endpoints'



export const Login = () => {   
    const { dispatch } = React.useContext(AuthContext)
    const initialState = {
        email: "",
        password: "",        
        isSubmitting: false,
        errorMessage: null,
        user:null     
    }

    const [data, setData] = React.useState(initialState)

    const handleInputChange = e => {        
        setData({
            ...data,
            [e.target.name]: e.target.value            
        })        
    }

    const handleFormSubmit = async e => {        
        setData({
            ...data,
            isSubmitting: true,
            errorMessage: null

        })

        try{

            const response = await api.user.login(data)

            dispatch({
                type: "LOGIN",
                payload: response
            })
            message.success(`Acceso correcto: ${response.user.first_name} ${response.user.last_name}`)
            
            
        } catch (error){            
            setData({isSubmitting:false, errorMessage:error.message || error.statusText})
            message.error('Credenciales Incorrectas')
            }   
        }

    return(
        <div className="general-login">
            
            
        
            <div className="login-container">
        <div className="login">
            <div className="head-login">
                <img alt='logo' src={logo} />
                <p style={{color:'white', opacity:'0.4', textAlign:'center'}}>CRM - Gestión de tareas y clientes.</p>
            </div>
            
        <Form
            onFinish = { handleFormSubmit }
            name="normal_login"
            className="login-form"
            initialValues={{ remember: true }}
            
            
        >
            <Form.Item
                name="email"
                rules={[{ required: true, message: 'Ingresa tu correo corporativo'}]}
            >
                <Input 
                    prefix={<UserOutlined className="site-form-item-icon" />}
                    type="email" 
                    placeholder="Email" 
                    value={data.email}
                    name="email"
                    onChange={handleInputChange}
                    
                />
            
            </Form.Item>

            <Form.Item
                name="password"
                rules={[{ required: true, message: 'Ingresa tu contraseña!' }]}
            >
                <Input
                    prefix={<LockOutlined className="site-form-item-icon" />}
                    type="password"
                    placeholder="Contraseña"
                    value={data.password}
                    name="password"                    
                    onChange={handleInputChange}

                />
            </Form.Item>
            <Form.Item>
                <Form.Item name="remember" valuePropName="checked" noStyle>
                <Checkbox>Recuerda mis datos</Checkbox>
                </Form.Item>

            
            </Form.Item>

            

            <Form.Item>
                
                {data.isSubmitting ? (<Spin />):(<Button type="primary" htmlType="submit" className="login-form-button">INGRESAR</Button>)}
                
                
             </Form.Item>
             
            
             
        </Form>
        
        
      

        </div>
        <p style={{color:'white'}}>2020 - Quality Net</p>
      </div>
        </div>
        
    )
}

export default Login