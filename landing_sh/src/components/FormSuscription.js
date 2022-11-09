import React, { useState, useEffect } from 'react'
import { Form, Typography, Select,
        notification, Row, Col, 
        Input, Button } from 'antd'
import { callbacks } from '../api/endpoints'

const { Title, Text } = Typography
const { Option } = Select

const FormSuscription = ({ closeAffix, is_affix, in_affix }) => {

    const initialState = {
        is_select_ocupation: false,
        string_ocupation: '',
        gender_other: false
    }

    const initialResponsive = {
        xs: 24, 
        sm: 12, 
        md: 12, 
        lg: 12, 
        xl: 12
    }

    const [form] = Form.useForm()

    const [state, setState] = useState(initialState)
    const [response, setResponse] = useState(initialResponsive)

    const onFinish = async(values) => {
        try {
            const request = await callbacks.signupEvent(values)
            notification.success({message: 'Inscripcion realizada correctamente'})
            form.resetFields()
            if(is_affix){                
                closeAffix(false)
            }
            return request
        } catch (error) {            
            notification.error({message: 'Error al procesar tu inscripcion'})   
        }
        
    }

    const resetForm = () => {
        form.resetFields()
        notification.warning({message:'Formulario reiniciado'})
    }

    useEffect(() => {
        if(in_affix){
            setResponse({
                ...response,                                
                lg: 6, 
                xl: 12,

            })
        }
    }, [])
    
    return(<>        
                <Form form={form} style={styles.form} layout={'vertical'} onFinish={onFinish}>
                    <Row>
                        <Col xs={response.xs} sm={response.sm} md={response.md} lg={response.lg} xl={response.xl} style={styles.col}>
                            <Form.Item name='name'
                                rules={[{ required: true, message: 'Ingresa tu nombre completo' }]} 
                                style={{color:'white'}} >
                                <Input placeholder='Nombre completo' />
                            </Form.Item>
                        </Col>
                        <Col xs={response.xs} sm={response.sm} md={response.md} lg={response.lg} xl={response.xl}style={styles.col}>
                            <Form.Item name='phone' 
                                rules={[{ required: true, message: 'Ingresa tu telefono'  }]} 
                                style={{color:'white'}}  >
                                <Input placeholder='Teléfono' />
                            </Form.Item>
                        </Col>
                        <Col xs={response.xs} sm={response.sm} md={response.md} lg={response.lg} xl={response.xl} style={styles.col}>
                            <Form.Item name='email' 
                                rules={[
                                    {
                                        required: true, 
                                        message: 'Ingresa tu correo electronico' 
                                    }, 
                                    {
                                        type: 'email',
                                        message: 'Recuerda ingresar tu @'
                                    }]} 
                                style={{color:'white'}} >
                                <Input placeholder='Correo' />
                            </Form.Item>
                        </Col>
                        <Col xs={response.xs} sm={response.sm} md={response.md} lg={response.lg} xl={response.xl} style={styles.col}>
                            <Form.Item name='commune'
                                rules={[{ required: true, message: 'Selecciona una opción' }]} 
                                style={{color:'white'}} >                        
                                <Select placeholder='Selecciona una opcion...'>                                
                                    <Option value='resdga'>Resolución DGA 1.238 MEE</Option>
                                    <Option value='bombeo'>Prueba Bombeo</Option>
                                    <Option value='aguanch'>Análisis de Agua NCh 409</Option>
                                    <Option value='insumos'>Insumos Planta APR</Option>
                                </Select>
                            </Form.Item>
                        </Col>
                        <Col span={24} style={styles.col}>
                            <Form.Item name='commune'
                                rules={[{ required: true, message: 'Selecciona una opción' }]} 
                                style={{color:'white'}}>                        
                              <Input.TextArea placeholder='Requerimiento...' />
                            </Form.Item>
                        </Col>                                                                         
                    </Row> 
                    <Row>
                        <Col>
                        <Button htmlType='submit' style={styles.btn} type='primary'>Enviar</Button>
                        </Col>
                        <Col>
                        <Button type='primary' style={styles.btn} onClick={resetForm}>Limpiar</Button>
                        </Col>
                    </Row>
                </Form>


    </>)

}

const styles = {
    col: {
        paddingLeft: '5px', paddingRight:'5px'
    },
    btn: {
        marginRight:'10px',
        marginBottom:'10px',
        borderRadius: '5px',
        backgroundColor:'#FCE921',
        borderColor:'#FCE921',
        color:'black'
    },
    form : {
        color:'white', 
        paddingLeft:'0px', 
        paddingRight:'0px',
        paddingTop:'70px'
    },
    container: {
        padding: '30px',
        paddingTop: '70px',
        paddingBottom:'60px'
    },
    title: {
        color:'white',
        textAlign: 'center'
    }, 
    text: {
        color: 'white',
    },
    label: {
        color: 'white'
    }
}


export default FormSuscription
