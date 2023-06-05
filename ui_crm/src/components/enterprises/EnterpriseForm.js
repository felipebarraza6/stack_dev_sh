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
        {attr.state.loading_form ? <Spin />: <Form 
                onFinish = {submitForm} 
                form = {form}
                >
                <Row justify='middle' >
                    <Col span={16} style={{marginTop:'20px'}} >
                        <Form.Item name="name" rules={[{ required: true, message: 'Ingresa el nombre de la empresa'}]} >
                            <Input name="name" prefix={<BuildOutlined/>} type="text" placeholder={'Nombre'}  />
                        </Form.Item>
                    </Col>
                    <Col span={8} style={{paddingLeft:'30px'}} >
                        <Button block style={{borderRadius:'10px', marginBottom:'10px'}}  type='primary' htmlType="submit">Crear cliente</Button>
                        <Button block  style={{borderRadius:'10px'}} onClick={clear} type>Limpiar</Button>
                        {attr.state.error && <Alert style={{margin:'20px'}} message='Ha ocurrido un error al crear el cliente' type="error" /> }                        
                        {attr.state.error && <Alert style={{margin:'20px'}} message={attr.state.error.response.data.email} type="error" /> }                                            
                    </Col>
                </Row>                
            </Form>}
            
        </div>
    )
}

export default EnterpriseForm
