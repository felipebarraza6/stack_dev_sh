import React from 'react'
import { Typography, Form, Row, 
    Col, Input, Select, Button,
    Card } from 'antd'

const FormFields = ({ section }) => {
    
    const [form] = Form.useForm()
    

    return(<Row>
        <Form form={form} onFinish={(values)=>console.log(values) } >{section &&<><Col span={24}>
            <Typography.Title level={3}>{section.name}</Typography.Title>
            <Typography.Paragraph level={3}>{section.description}</Typography.Paragraph>
        </Col>
        <Col span={24}>
            {section.fields.map((field)=> {
                return (<Form.Item name={field.name_field} label={field.type !== 'FILE' && field.label}>
                    {field.type === 'SELECT' && <Select placeholder={field.help_text}>
                        {field.options.map((option)=> 
                        <Select.Option value={option.name}>{option.name}</Select.Option>
                    )}                    
                    </Select>}                    
                    {field.type === 'TEXT' && <>
                        <Input placeholder={field.help_text} />
                        </>}
                    {field.type === 'FILE' && <Card hoverable>
                        <Typography.Paragraph ><b>{field.label}</b></Typography.Paragraph>
                        <input type='file' /><label>INDICACIONES: {field.help_text}</label>
                        </Card>}
                </Form.Item>)
            })}
        </Col>
        <Col>
            {!section.is_file_section && <>
              <Button type='primary' htmlType={'submit'} disabled={section.is_complete}>GUARDAR</Button>
              <Button onClick={()=> form.resetFields()} style={styles.clearBtn} disabled={section.is_complete}>LIMPIAR</Button>
            </>
            }

        </Col>
    </>}</Form>
    </Row>)

}

const styles = {
  clearBtn : {
    marginLeft:'10px'
  }
}


export default FormFields
