import React, { useState } from 'react'
import { Modal, Button, Form, Input, notification } from 'antd'
import api from '../../../api/endpoints'

const UpdateFile = ({properties, file, count, setCount}) => {

    const [visible, setVisible] = useState(false)
    const [form] = Form.useForm()


    const onUpdate = async(values) => {        
        console.log(file)
        const rq = await api.projects.values_elements.update(file, values).then((r)=>{
            
            setCount(count+1)
            notification.success({message:'Campos actualizados!'})
            form.resetFields()
            setVisible(false)            
        
    })
}

    return(<>
        <Modal visible={visible} onCancel={()=>setVisible(false)} footer={[]} title={file.name} >
            <Form onFinish={onUpdate} form={form} style={{paddingRight:'20px', paddingLeft:'20px'}} initialValues={file}>
                <Form.Item name={'name'} rules={[{required: true, message:'Campo obligatorio'}]}>
                    <Input />
                </Form.Item>
                <Form.Item name={'code'} rules={[{required: true, message:'Campo obligatorio'}]}>
                    <Input />
                </Form.Item>
                <Form.Item name={'note'}>
                    <Input.TextArea />
                </Form.Item>
                <Form.Item>
                    <Button htmlType='submit' type="primary" size="small" style={{ margin: "5px", backgroundColor: properties&&properties.color, borderColor: properties&&properties.color }} onClick={()=>setVisible(true)}>Guardar</Button> 
                </Form.Item>
            </Form>            
        </Modal>
        <Button type="primary" size="small" style={{ margin: "5px", backgroundColor: properties&&properties.color, borderColor: properties&&properties.color }} onClick={()=>setVisible(true)}>Modificar</Button>
    </>)

}


export default UpdateFile