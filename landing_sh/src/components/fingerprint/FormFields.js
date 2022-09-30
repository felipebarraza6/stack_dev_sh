import React, { useState } from 'react'
import { Typography, Form, Row, 
    Col, Input, Select, Button,
    Card, Upload, notification, Spin, List, Tag, Badge } from 'antd'

import { callbacks } from '../../api/endpoints'
import Wells from '../dgaform/Wells'
import { BASE_URL, BASE_URL_MEDIA } from '../../api/config'
import img_pozo from '../../assets/images/dem1.png'

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

    async function addFile(upload, field){
      const request = await callbacks.fingerprint.update_file(`${BASE_URL}fields/${field}/`, upload.file.originFileObj)
      if(request.status==200){
        notification.success({message: 'ARCHIVO CARGADO CORRECTAMENTE'})
      }
    }
    return(<Row>
        <Form form={form} onFinish={onFinish} >{section &&<><Col span={24}>
            <Typography.Title level={3}>{section.name}</Typography.Title>
            <Typography.Paragraph level={3}>{section.description}</Typography.Paragraph>
        </Col>
          <Col span={24} style={{color:'white'}}>----------------------------------------------------------------------------------------------------------------------------------------</Col>

          {section.is_captation_data && <Row>
                          <Col span={12}>
                              <List bordered style={{marginTop:'0px'}}>
                                  <List.Item>1 - Caudal otorgado: <Tag color='blue'>Lt/SEG</Tag></List.Item>
                                  <List.Item>2 - Profundidad total del pozo: <Tag color='blue'>Mt</Tag></List.Item>
                                  <List.Item>3 - Nivel Estático: <Tag color='blue'>Mt</Tag></List.Item>
                                  <List.Item>4 - Nivel Dinámico: <Tag color='blue'>Mt</Tag></List.Item>
                                  <List.Item>5 - Profundidad instalacion bomda: <Tag color='blue'>Mt</Tag></List.Item>
                                  <List.Item>6 - Diámetro interior pozo: <Tag color='blue'>MM/PULG</Tag></List.Item>
                                  <List.Item>7 - Diámetro exterior ducto salida bomba: <Tag color='blue'>MM/PULG</Tag></List.Item>
                              </List>
                            </Col>                            
                            <Col span={12} style={styles.col_well}>
                                <Input style={{...styles.input, marginTop:'70px', marginLeft:'60px'}} prefix={<Badge count={1} style={styles.badgeNumber} />} />
                                <Input style={{...styles.input, marginTop:'290px', marginLeft:'120px'}} prefix={<Badge count={2} style={styles.badgeNumber} />} />
                                <Input style={{...styles.input, marginTop:'200px', marginLeft:'290px'}} prefix={<Badge count={3} style={styles.badgeNumber} />} />
                                <Input style={{...styles.input, marginLeft:'295px', marginTop:'260px'}} prefix={<Badge count={4} style={styles.badgeNumber} />} />
                                <Input style={{...styles.input, marginTop:'320px', marginLeft:'290px'}} prefix={<Badge count={5} style={styles.badgeNumber} />} />
                                <Input style={{...styles.input, marginTop:'150px', marginLeft:'290px'}} prefix={<Badge count={6} style={styles.badgeNumber} />} />
                                <Input style={{...styles.input, marginTop:'80px', marginLeft:'290px'}} prefix={<Badge count={7} style={styles.badgeNumber} />} />
                            </Col>
            </Row>}
        <Col span={12}>
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
                        <Typography.Paragraph>
                        {field.label}</Typography.Paragraph>
                        {field.file && <Button type='primary' onClick={()=> window.open(`${BASE_URL_MEDIA}${field.file.slice(1)}`) } >DESCARGAR ARCHIVO</Button>}
                        <Upload onChange={(e)=>addFile(e, field.id)} name={field.id} maxCount={1}>
                          <Button icon={<span style={styles.span}>+</span>} > CLICK PARA SUBIR ARCHIVO</Button>
                        </Upload>
                        <Input.TextArea style={{ marginTop:'10px' }} placeholder="Agregar un comentario..." />
                        {field.label !== 'Documentación' && 
                        <Button type={'primary'} onClick={()=> window.open('https://www.registrodeempresasysociedades.cl/')} style={{ marginTop:'10px' }} placeholder="">¿Donde obtener?</Button>}
                      </Card>}
                </Form.Item>)
            })}
        </Col>
        <Col>
            {!section.is_file_section && <>
              <Button  type='primary' htmlType={'submit'} disabled={section.is_complete || section.in_validate}>GUARDAR</Button>
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
  },
col_well: {
    backgroundImage: `url(${img_pozo})`,
    backgroundPosition: 'center',
    backgroundSize: '180% auto',
    height: '450px',
    backgroundRepeat: 'no-repeat',
    width: '100%',
    marginTop: window.innerWidth > 800 ? '0px': '20px'
  },
  input: {
    position: 'absolute',
    width: '25%',
  },
  badgeNumber: {
    backgroundColor: '#1890ff',
  },
  img_well:{
    backgroundImage: `url${img_pozo}`,
    backgroundPosition: 'center',
    backgroundSize: '100% auto',
    height: '300px',
    width: '100%',
    backgroundRepeat: 'no-repeat',
    marginTop: '100px',
  },
  col_datas: {
    padding:'0px',
  },
  col_datas_b: {
    paddingleft: '10px',
    paddingright: '10px',
    marginbottom: '100px',
  },
  col_tech: {
    padding: '3px'
  }
}


export default FormFields
