import React from 'react'
import { Form, Input, Select, Button, Row, Col, Spin, Alert } from 'antd';

import { BuildOutlined, MailOutlined,  } from '@ant-design/icons'

import { postEnterprise } from '../../actions/enterprises'

const { Option } = Select


const EnterpriseForm = (attr) =>{    
    
    const [form] = Form.useForm()

    const submitForm = (data) =>{
        
        postEnterprise(attr.dispatch, data, attr.state.page)                                        
        form.resetFields()
    }
    
    const clear = () => {
        form.resetFields()
    }

    return(
        <div className="steps-content"> 
        { attr.state.loading_form ? <Spin />: <Form 
                onFinish = {submitForm} 
                form = {form}
                >
                <Row>
                    <Col span={16}>
                        <Form.Item name="name" rules={[{ required: true, message: 'Ingresa el nombre de la empresa'}]} >
                            <Input name="name" prefix={<BuildOutlined/>} type="text" placeholder={'Nombre'}  />
                        </Form.Item>
                        <Row>
                            <Col span={12}>
                                <Form.Item  name="type_client" rules={[{ required: true, message: 'Selecciona una tipo de empresa'}]} >
                                    <Select name="type_client" placeholder="Selecciona un tipo de cliente" style={{marginRight:'5px'}}>                
                                        <Option value="Empresa">Empresa</Option>
                                        <Option value="Planta APR">Planta APR</Option>
                                        <Option value="Municipio">Municipalidad</Option>
                                        <Option value="Essbio">Essbio</Option>
                                        <Option value="DOH">DOH</Option>                                                     
                                    </Select>                                    
                                </Form.Item>
                            </Col>                            
                            <Col span={12}>
                                <Form.Item name="email" rules={[{ type:"email", required: true, message: 'Ingresa el correo electrónico'}]} >
                                    <Input name="email" prefix={<MailOutlined />} type="email" placeholder="Email" style={{marginLeft:'5px'}}/>
                                </Form.Item>    
                            </Col>
                        </Row>                        
                    </Col >
                    <Col span={8}>
                        <Button style={{marginRight: '5px', marginLeft: '15px'}} type='primary' htmlType="submit">Crear</Button>
                        <Button style={{marginRight: '5px' }} onClick={clear} type>Limpiar</Button>
                        {attr.state.error && <Alert style={{margin:'20px'}} message='Ha ocurrido un error al crear el cliente' type="error" /> }                        
                        {attr.state.error && <Alert style={{margin:'20px'}} message={attr.state.error.response.data.email} type="error" /> }                                            
                    </Col>
                </Row>                
            </Form>                }
            
        </div>
    )
}

export default EnterpriseForm