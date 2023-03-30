import React, { useContext, useEffect, useState } from 'react'
import { Form, Typography, Input, 
        Select, Button, notification } from 'antd'
import { QuotationContext } from '../../../containers/Quotation'
import { InternalLiftingContext } from '../../pages/InternalLifting'
import { ArrowRightOutlined, ArrowLeftOutlined } from '@ant-design/icons'

const { Title, Paragraph } = Typography

const AddWell = () => {
  
  const [form] = Form.useForm()
  
  const [coordinates, setCoordinates] = useState({
    latitude: '-00.00000000000000',
    longitude: '-00.00000000000000',
  })

  const { state, dispatch } = useContext(InternalLiftingContext)

  const onFinishFormGeneral = (values) => {    
    values = {
      name_well: values.name_well.toUpperCase(),
      type_captation: values.type_captation.toUpperCase(),
      address_exact: values.address_exact.toUpperCase()
    }

    if(state.wells.list.length>0 && !state.wells.temporary_well.is_edit){

      state.wells.list.map((x)=> {        
        if(x.general_data.name_well === values.name_well){
          notification.warning({message:'Ya tienes un pozo agregado con este nombre'})
        }else {
          dispatch({ 
            type: 'ADD_GENERAL_DATA',
            data: values
          })
        }
      })

    } else {
      dispatch({ 
        type: 'ADD_GENERAL_DATA',
        data: values
      })
    }
    

    
  }

  useEffect(()=>{
    navigator.geolocation.getCurrentPosition(
      async(position) => {
        console.log(position)
        setCoordinates({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
      },
      (error) => console.error(error)
    ); 
  },[])
  


  return(<Form initialValues={state.wells.temporary_well.general_data} layout={'vertical'} form={form} onFinish={onFinishFormGeneral}>
          <Title level={3}>Ingresa los datos iniciales de tu pozo...</Title>
          <Paragraph>{coordinates && <>Latitud: {coordinates.latitude}</>}</Paragraph>
          <Paragraph>{coordinates && <>Longitud: {coordinates.longitude}</>}</Paragraph>
          <Form.Item label='Nombre del pozo' name='name_well' 
            rules={[{ required: true, message:'Debes ingresar el nombre' }]}>
            <Input placeholder='Ingresa el nombre de tu pozo' />
          </Form.Item>
          <Form.Item label='Tipo de captación' name='type_captation' 
            rules={[{ required: true, message:'Selecciona un tipo de captación' }]}>
            <Select placeholder='Selecciona un tipo de captación'>
              <Select.Option value='pozo'>Pozo</Select.Option>
              <Select.Option value='puntera'>Puntera</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item label='Dirección o ubicación del pozo' name='address_exact' 
            rules={[{ required: true, message:'Ingresa la dirección del pozo' }]}>
            <Input.TextArea placeholder='Región, comuna, sector, calle #123'  rows={4} />
          </Form.Item>
          <Button style={styles.btnP} htmlType="submit" type='primary' icon={state.wells.temporary_well.general_data ? <ArrowLeftOutlined/>:<ArrowRightOutlined />}>
            {state.wells.temporary_well.general_data ? 'Actualizar datos generales y continuar':'Siguiente'} 
          </Button>
          {!state.wells.temporary_well.general_data && 
          <Button style={styles.btnP} onClick={()=> form.resetFields()}>Limpiar</Button>          
          }
          {state.wells.list.length > 0 & !state.wells.temporary_well.general_data ?
            <Button type='primary' danger style={styles.btnP} onClick={()=> dispatch({type:'SET_CURRENT', step:2})}>Cancelar</Button>:
            <>{state.wells.list.length>0 &&            
            <Button type='primary' danger style={styles.btnP} onClick={()=> dispatch({type:'CHANGE_CREATE_OR_EDIT', option:false})}>Cancelar</Button>
            }
            </>
          }
    </Form>)
}

const styles = {
  btnP: {
    margin:'10px'
  }
}

export default AddWell
