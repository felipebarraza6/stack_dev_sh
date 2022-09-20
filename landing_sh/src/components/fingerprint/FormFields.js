import React from 'react'
import { Typography, Form, Row, 
    Col, Input, Select, Button,
    Card, Upload } from 'antd'

const FormFields = ({ section }) => {
    
    const [form] = Form.useForm()

    function onFinish(values){
      console.log(values)
    }

    function changeValue(value, field){
      form.setFieldsValue({
        [field]: value
      })
    }

    function addFile(file, field){
      console.log(file.target.files)
      console.log(field)
    }

    return(<Row>
        <Form form={form} onFinish={onFinish} >{section &&<><Col span={24}>
            <Typography.Title level={3}>{section.name}</Typography.Title>
            <Typography.Paragraph level={3}>{section.description}</Typography.Paragraph>
        </Col>
        <Col span={24}>
            {section.fields.map((field)=> {
                console.log(field)
                return (<Form.Item name={field.name_field} label={field.type !== 'FILE' && field.label}>
                    {field.type === 'SELECT' && <Select name='select' 
                        onChange={(value)=>changeValue(value, field.name_field)} 
                        placeholder={field.help_text} allowClear>
                        {field.options.map((option)=> {  
                          return(<Select.Option value={option.name}>{option.name}</Select.Option>)
                        }
                    )}                    
                    </Select>}                    
                    {field.type === 'TEXT' && <>
                        <Input placeholder={field.help_text} onChange={(e)=>changeValue(e.target.value, field.name_field)} />
                      </>}
                    {field.type === 'FILE' && <Card hoverable>
                        <Typography.Paragraph bold>
                        {field.label}</Typography.Paragraph>
                        <Upload onChange={(e)=>console.log(e)} name="avatar" maxCount={1}>
                          <Button icon={<span style={styles.span}>+</span>} > CLICK PARA SUBIR ARCHIVO</Button>
                        </Upload>
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
  },
  span: {
    marginRight: '10px',
    fontSize: '14px'
  }
}


export default FormFields
