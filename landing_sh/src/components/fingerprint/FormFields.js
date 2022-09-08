import React from 'react'
import { Typography, Form, Row, 
    Col, Input, Select, Button } from 'antd'

const FormFields = ({ section }) => {
    
    return(<Row>
        <Form>{section &&<><Col span={24}>
            <Typography.Title level={3}>{section.name}</Typography.Title>
            <Typography.Paragraph level={3}>{section.description}</Typography.Paragraph>
        </Col>
        <Col span={24}>
            {section.fields.map((field)=> {
                return (<Form.Item label={field.type !== 'FILE' && field.label}>
                    
                    {field.type== 'SELECT' && <Select placeholder={field.help_text}>
                        {field.options.map((option)=> 
                        <Select.Option value={option.name}>{option.name}</Select.Option>
                    )}                    
                    </Select>}                    
                    {field.type === 'TEXT' && <>
                        <Input placeholder={field.help_text} />
                        </>}
                    {field.type === 'FILE' && <>
                        <Typography.Paragraph ><b>{field.label}</b></Typography.Paragraph>
                        <input type='file' /><label>INDICACIONES: {field.help_text}</label></>}
                    
                </Form.Item>)
            })}
        </Col>
        <Col>
            <Button type='primary' disabled={section.is_complete}>GUARDAR</Button>
        </Col>
    </>}</Form>
    </Row>)

}


export default FormFields
