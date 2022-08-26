import React, { useState } from 'react'
import { Form, Input, Row, Space, 
        Col, Button, Modal } from 'antd'
import { callbacks } from '../../api/endpoints' 
const { Item } = Form

const FormClientExternal = ({ setDataClient,isModal, is_public,setStatusSub, setSteps, setQuotation }) => {
  
  const [form] = Form.useForm()
  const [isCreate ,setIsCreate] = useState(false)

  async function onFinish(data) {
    const rq = await callbacks.external_clients.create(data)
      .then((res)=>{
        setIsCreate(true)
        if(isModal){
          Modal.destroyAll()
          setStatusSub(true)
        } else {
          setDataClient(res)
          const createQuo = async()=> {
            const rq = await callbacks.quotation.create({ 
              external_client: res.data.id,
              is_external_client: true
            }).then((res)=> setQuotation(res.data.uuid))
            return rq
          }
          createQuo()
        }
      
      })
      return rq
    }
  

  return(<div >
      <Form layout={'vertical'} form={form} onFinish={onFinish}>
        <Item  label='Nombre Empresa' name='name_enterprise' rules={[{ required: true, message:'campo obligatorio' }]}>
          <Input disabled={isCreate} />
        </Item>
        <Item label='Dirección Empresa' name='address_enterprise' rules={[{ required: true, message:'campo obligatorio' }]}>
          <Input disabled={isCreate} placeholder={'REGION, COMUNA Y SECTOR O CALLE ‘METROPOLITANA, ISLA DE MAIPO Y LA ISLITA’'} />
        </Item>
        <Item label='Nombre Contacto' name='name_contact' rules={[{ required: true, message:'campo obliatorio' }]}>
          <Input disabled={isCreate} />
        </Item>
        <Item label='Email Contacto' name='mail_contact' rules={[{ type:'email',required: true, message:'campo obliatorio' }]}>
          <Input disabled={isCreate} />
        </Item>
        <Item label='Telefono Contacto' name='phone_contact' rules={[{ required: true, message:'campo obliatorio' }]}>
          <Input disabled={isCreate} />
        </Item>
        <Item style={styles.itemBtn}>
          <Button style={styles.btn} disabled={isCreate} type='primary' htmlType='submit'>ENVÍAR</Button>
          {!isCreate && 
            <Button type='primary' danger onClick={()=> form.resetFields()} >LIMPIAR DATOS</Button>
          }
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
