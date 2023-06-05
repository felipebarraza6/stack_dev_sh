import React, { useState, useEffect } from 'react'
import { Form, Input, Select, Button, Card, notification } from 'antd'
import api from '../../api/endpoints'
import { FilePdfOutlined, FileExcelOutlined, 
        FileWordOutlined, FileImageOutlined,
        FilePptOutlined } from '@ant-design/icons'

const { Option } = Select

const FormElement = ({ count, setCount, selectElement, setSelectElement }) => {

    const [form] = Form.useForm()

    const [updateForm, setUpdateForm] = useState(false)

    const onCreate = async(values) => {
        if(values.type==='is_file'){
            values = {
                ...values,
                is_file:true,
                is_info:false
            }
        } else {
            values = {
                ...values,
                is_file:false,
                is_info:true
            }
        }
        
        if(selectElement){
          console.log(selectElement)
            const rq = await api.projects.types_elements.update(selectElement.id, values).then((r)=> {
              notification.success({message:'Entrada actualizada correctamente'})
              setSelectElement(null)
              setCount(count+1)
              form.resetFields()
            })
        }else {
            const rq = await api.projects.types_elements.create(values).then((r)=> {
            console.log(r)
            setCount(count+1)
            form.resetFields()
            notification.success({message:'Entrada creada correctamente!'})
        })

        }

        
    }

    useEffect(()=> {
        if(selectElement){
            setUpdateForm(true)
            setTimeout(() => {
                setUpdateForm(false)
              }, 1000);
        }
    }, [selectElement])

    return(<Card hoverable bordered>
        {!updateForm && 
        <Form initialValues={selectElement} form={form} onFinish={onCreate} layout='vertical' style={{padding:'10px'}}>
        <Form.Item label='Nombre visible' name='name' rules={[{required:true, message:'Ingresa el nombre...'}]}>
            <Input />
        </Form.Item>
        <Form.Item label='Descripción' name='description' >
            <Input.TextArea rows={4} />
        </Form.Item>
        <Form.Item label='Tipo entrada' name='type' rules={[{required:true, message:'Selecciona una opcion...'}]}>
            <Select placeholder='Debes seleccionar el tipo de entrada'>
                <Option value='is_file'>Archivo</Option>
                <Option value='is_info'>Información</Option>
            </Select>
        </Form.Item>   
        <Form.Item label='Tipo archivo' name='type_file' rules={[{required:true, message:'Selecciona una opcion...'}]}>
            <Select placeholder='Debes seleccionar el tipo de archivo'>
                <Option value='pdf'><FilePdfOutlined style={{fontSize:'16px', color:'red'}} /> PDF</Option>
                <Option value='word'><FileWordOutlined style={{fontSize:'16px', color:'blue'}} /> WORD</Option>
                <Option value='excel'><FileExcelOutlined style={{fontSize:'16px', color:'green'}} /> EXCEL</Option>
                <Option value='powerpoint'><FileExcelOutlined style={{fontSize:'16px', color:'orange'}} /> POWER POINT</Option>
                <Option value='image'><FileImageOutlined style={{fontSize:'16px', color:'purple'}} /> IMGAGEN</Option>
                <Option value='s/n'>SIN TIPO DE ARCHIVO</Option>
            </Select>
        </Form.Item>  
        <Form.Item label='Posicion' name='position'>
          <Input type='number' /> 
        </Form.Item>
        <Form.Item>
            <Button htmlType='submit' type='primary' style={{marginRight:'10px'}}>Guardar</Button>
            <Button onClick={()=>form.resetFields()}>Limpiar</Button>
        </Form.Item></Form> }
    </Card>)

}


export default FormElement
