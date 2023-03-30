import React, { useState, useContext, useEffect } from 'react'
import { Form, Input, Button,Modal,Spin, Typography, Row,Col,Select, notification } from 'antd'
import { QuotationContext } from '../../containers/Quotation'
import { InternalLiftingContext } from '../pages/InternalLifting'
import { ArrowUpOutlined, ArrowRightOutlined, ArrowLeftOutlined, PlayCircleOutlined, PlaySquareOutlined } from '@ant-design/icons'
import { callbacks } from '../../api/endpoints'
const { Item } = Form
const { Title } = Typography





const FormClient = () => {
  
  const { state, dispatch } = useContext(InternalLiftingContext)
  const [form] = Form.useForm()
  const [sendData, setSendData] = useState(false)
  const [dataform, setDataform] = useState(null)
  const [clients, setClients] = useState(null)
  const [visible, setVisible] = useState(false)

  const sendAllData = () => {
    console.log(state)
    console.log(dataform)
  }

  const senData = async() => {
    setVisible(true)
    console.log(state.wells.list)
    const rq1_create_client = await callbacks.external_clients.create({...state.client}).then((response)=>{            
        notification.success({message: 'DATOS DE CONTACTO'})           
        const rq2_create_quotation =  callbacks.quotation.create({
            external_client: response.data.id,
            is_client: true,            
            client: dataform.client
        }).then((response)=>{                
            notification.success({message: `${response.data.uuid} ID UNICO EN NUESTRA API`})           
            var list_with_quotation_uui = (list) => {
                var list_f = []            
                list.map((well)=> {
                    list_f.push({
                        ...well,
                        quotation: response.data.uuid
                    })
                })            
                return list_f            
            }
    
            const r3_create_wells = callbacks.quotation.createWell(list_with_quotation_uui(state.wells.list)).then((r)=> {
                setTimeout(() => {
                    window.location.reload()
                }, 5000);
            })
        })
    })
}
  
  async function onFinish(data) {    
    dispatch({
      type: 'SET_CLIENT',
      client: data
    })
    setSendData(true)    
    dispatch({
      type: 'SET_VALIDATED_CONTACT',
    })
    setDataform(data)
 
  }

  const getData=async()=> {
    const rq1=await callbacks.clients.list().then((r)=> {
      console.log(r.results)
      setClients(r.results)
    })
  }

  useEffect(()=>{
    getData()
  }, [])

  
  return(<div >
    <Modal visible={visible} onCancel={()=>setVisible(false)} footer={[]} width={'650px'} centered>
                <Row justify="center">
                    <Col span={24}>
                        <center><Typography.Title level={3}>
                        DATOS CARGADOS CORRECTAMENTE, SE ACTUALIZARA LA APP
                        </Typography.Title></center>
                    </Col>
                    <Col span={24} style={{marginLeft:'95%', marginTop:'40px', marginBottom:'40px'}}>
                        <Spin size='large' />                        
                    </Col>
                    <Col span={24}><center>
                        
                        </center>
                    </Col>
                </Row>
            </Modal>
      <Form name='form_person' layout={'vertical'} style={{marginTop:window.innerWidth>900&&'100px'}} 
          form={form} onFinish={onFinish} initialValues={state.client}>        
        <Title level={3}>Ingresa al receptor de visita...</Title>
        <Item label='Nombre Contacto' name='name_contact' rules={[{ required: true, message:'campo obliatorio' }]}>
          <Input />
        </Item>
        <Item label='Email Contacto' name='mail_contact' rules={[{ type:'email',required: true, message:'campo obliatorio' }]}>
          <Input />
        </Item>
        <Item label='Teléfono Contacto' name='phone_contact' rules={[{ required: true, message:'campo obliatorio' }]}>
          <Input />
        </Item>
        <Title level={5}>Selecciona al cliente que corresponde está visita</Title>
        <Item name='client'>
          <Select placeholder='Selecciona a un cliente...'>
            {clients && <>
              {clients.map((c)=><Select.Option value={c.id}>
                {c.name}
              </Select.Option>)}
            </>}            
          </Select>
        </Item>
        <Item style={styles.itemBtn}>
          {state.client ?
            <Button style={styles.btn} type='primary' htmlType='submit' icon={<ArrowLeftOutlined />}>Actualizar </Button>:
             <Button style={styles.btn} type='primary' htmlType='submit' icon={<ArrowUpOutlined />} >Aceptar</Button>
          }          
          {!state.client && <Button onClick={()=> form.resetFields()} >Limpiar</Button>}
          {sendData ?
          <Button style={styles.btn2} type='primary' onClick={()=>senData()} icon={<PlayCircleOutlined />} >Enviar datos y finalizar</Button>:
          <Button style={styles.btn2} type='primary' onClick={()=>dispatch({type:'SET_CURRENT', step:2})} icon={<ArrowLeftOutlined />} >Volver</Button>          
          } 
          
        </Item>        
      </Form>
  </div>)
}


const styles = {
  btn: {
    marginRight: '10px'
  },
  btn2: {
    marginLeft: '10px'
  },
  itemBtn: {
    marginTop: '20px'
  }
}


export default FormClient
