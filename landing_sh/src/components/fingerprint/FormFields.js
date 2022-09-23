import React, { useState } from 'react'
import { Typography, Form, Row, 
    Col, Input, Select, Button,
    Card, Upload, notification, Spin } from 'antd'

import {callbacks} from '../../api/endpoints'

const FormFields = ({ section }) => {
    
    const [form] = Form.useForm()
    const [isLoading, setIsLoading] = useState(false)

    async function onFinish(values){
      setIsLoading(true)
      try {
          for (const property in values) {
            console.log(property)
            const rq = await callbacks.fingerprint.update_field(
              property, 
              { 
                value: values[property] 
              }).then((res)=> {

              })
          }
        setIsLoading(false)
        notification.success({message: 'LOS DATOS SE CARGARON CORRECTAMENTE'})
      } catch(error){
        notification.error({ message: 'ERROR AL CARGAR DATOS!' })
        setIsLoading(false)
      }

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
                return (<Form.Item name={field.id} label={field.type !== 'FILE' && field.label}>
                    {field.type === 'SELECT' && <Select defaultValue={field.value} name='select' 
                        onChange={(value)=>changeValue(value, field.id)} 
                        placeholder={field.help_text} allowClear>
                        {field.options.map((option)=> {  
                          return(<Select.Option value={option.name}>{option.name}</Select.Option>)
                        }
                    )}                    
                    </Select>}                    
                    {field.type === 'TEXT' && <>
                        <Input defaultValue={field.value} placeholder={field.help_text} onChange={(e)=>changeValue(e.target.value, field.id)} />
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
              <Button  type='primary' htmlType={'submit'} disabled={section.is_complete || isLoading}>GUARDAR</Button>
              {isLoading && <Spin style={styles.spin} size="default" />}
            </>
            }

        </Col>
    </>}</Form>
    </Row>)

}

const styles = {
  spin: {
    marginLeft: '20px'
  },
  clearBtn : {
    marginLeft:'10px'
  },
  span: {
    marginRight: '10px',
    fontSize: '14px'
  }
}


export default FormFields
