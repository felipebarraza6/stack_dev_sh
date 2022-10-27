import React, { useContext, useState } from 'react'
import { QuotationContext } from '../../../containers/QuotationExternalClients'
import { Form, Typography, Input, 
        Select, Button } from 'antd'

const { Title } = Typography

const AddWell = () => {
  
  const { state, dispatch } = useContext(QuotationContext)

  const initialState = {
    general: null,
    data_well: null
  }
  
  const [data, setData] = useState(initialState)
  const [form] = Form.useForm()

  const onFinishFormGeneral = (values) => {
    setData({
      ...data,
      general: values 
    })
  }

  console.log(data)

  return(<Form layout={'vertical'} form={form} onFinish={onFinishFormGeneral}>
          <Title level={3}>Ingresa los datos iniciales de tu pozo...</Title>
          <Form.Item label='Nombre del pozo' name='name_well' 
            rules={[{ required: true, message:'campo obligatorio' }]}>
            <Input placeholder='Ingresa el nombre de tu pozo' />
          </Form.Item>
          <Form.Item label='Tipo de captación' name='type_captation' 
            rules={[{ required: true, message:'campo obligatorio' }]}>
            <Select placeholder='Selecciona un tipo de captación'>
              <Select.Option value='pozo'>Pozo</Select.Option>
              <Select.Option value='puntera'>Puntera</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item label='Dirección o ubicación del pozo' name='address_exact' 
            rules={[{ required: true, message:'campo obligatorio' }]}>
            <Input.TextArea placeholder='Región, comuna, sector, calle #123'  rows={4} />
          </Form.Item>
          <Button style={styles.btnP} htmlType="submit" type='primary'>Siguiente</Button>
          <Button style={styles.btnP} onClick={()=> form.resetFields()}>Limpiar</Button>
    </Form>)
}

const styles = {
  btnP: {
    margin:'10px'
  }
}

export default AddWell
