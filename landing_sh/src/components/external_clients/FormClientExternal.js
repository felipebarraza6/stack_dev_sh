import React, { useState, useContext } from 'react'
import { Form, Input, Button } from 'antd'
import { QuotationContext } from '../../containers/Quotation'
import { ArrowRightOutlined, ArrowLeftOutlined } from '@ant-design/icons'
const { Item } = Form

const FormClientExternal = () => {
  
  const { state, dispatch } = useContext(QuotationContext)
  const [form] = Form.useForm()
  
  async function onFinish(data) {    
    dispatch({
      type: 'SET_CLIENT',
      client: data
    })
    dispatch({
      type: 'SET_CURRENT',
      step: state.wells.list.length > 0 ? state.wells.temporary_well.general_data ? 1:2:1
    })
    dispatch({
      type: 'SET_VALIDATED_CONTACT',
    })
    dispatch({
      type: 'SET_STEP_01',
      finish: true,
      active: false,
      hide: false
    })
    
    /*
    const rq = await callbacks.external_clients.create(data)
      .then((res)=>{
        setIsCreate(true)
          const createQuo = async() => {
            const rq = await callbacks.quotation.create({ 
              external_client: res.data.id,
              is_external_client: true
            }).then((res)=> console.log(res))
            return rq          
        }
        createQuo()
    })
    return rq
    */
  }

  
  return(<div >
      <Form name='form_person' layout={'vertical'} 
          form={form} onFinish={onFinish} initialValues={state.client}>
        <Item  label='Nombre Empresa' name='name_enterprise' rules={[{ required: true, message:'campo obligatorio' }]}>
          <Input />
        </Item>
        <Item label='Nombre Contacto' name='name_contact' rules={[{ required: true, message:'campo obliatorio' }]}>
          <Input />
        </Item>
        <Item label='Email Contacto' name='mail_contact' rules={[{ type:'email',required: true, message:'campo obliatorio' }]}>
          <Input />
        </Item>
        <Item label='Teléfono Contacto' name='phone_contact' rules={[{ required: true, message:'campo obliatorio' }]}>
          <Input />
        </Item>
        <Item style={styles.itemBtn}>
          {state.client ?
            <Button style={styles.btn} type='primary' htmlType='submit' icon={<ArrowLeftOutlined />}>Actualizar datos y volver</Button>:
             <Button style={styles.btn} type='primary' htmlType='submit' icon={<ArrowRightOutlined />} >Siguiente</Button>
          }          
          {!state.client && <Button onClick={()=> form.resetFields()} >Limpiar</Button>}
          
        </Item>
      </Form>
  </div>)
}


const styles = {
  btn: {
    marginRight: '10px'
  },
  itemBtn: {
    marginTop: '20px'
  }
}


export default FormClientExternal
