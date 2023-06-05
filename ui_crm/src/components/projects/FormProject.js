import React, { useState, useEffect } from 'react'
import api from '../../api/endpoints'
import { Form, Input, Card, Select, Button, notification } from 'antd'
const { Option } = Select

const FormProject = ({setCount, count, selectProject, setSelectClient}) => {

    console.log(selectProject)

    const [enterprises, setEnterprises] = useState(null)    
    const [updateForm, setUpdateForm] = useState(false)

    const [form] = Form.useForm()

    const getClients = async()=> {
        const rq1 = api.enterprises.get_total_enterprises().then((e)=>setEnterprises(e.enterprises_actives.data.results))
    }

    const onFinish = async(values) => {
        console.log(values)
        if(!selectProject){
            const rq1 = api.projects.project.create(values).then((res)=> {
                console.log(res)
                notification.success({message:'Proyecto creado correctamente!'})
                setCount(count+1)
                form.resetFields()
            })
        } else {
            const rq1 = api.projects.project.update(selectProject.id, values).then((res)=> {
                console.log(res)
                notification.success({message:'Proyecto actualizado correctamente!'})
                setCount(count+1)
                setSelectClient(null)
                form.resetFields()
            }) 
        }
        
    }

    useEffect(()=> {
        getClients()
        if(selectProject){
            setUpdateForm(true)
            setTimeout(() => {
                setUpdateForm(false)
              }, 1000);
        }
    }, [selectProject])

    return(<>
        <Card hoverable bordered>
            {!updateForm && 
            <Form layout='vertical' onFinish={onFinish} form={form} initialValues={selectProject}>
                <Form.Item label="Cliente" name="client" rules={[{required:true}]}>
                    <Select placeholder="Selecciona un cliente">
                        {enterprises &&
                            enterprises.map((x)=><Option key="x.id" value={x.id}>{x.name}</Option>)                            
                        }
                    </Select>
                </Form.Item>
                <Form.Item label="Nombre proyecto" name="name" rules={[{required:true}]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Codigo interno" name="code_internal" rules={[{required:true}]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Descripción" name="description">
                    <Input.TextArea rows={4} />
                </Form.Item>
                <Form.Item>
                    <Button htmlType='submit' type="primary">Guardar proyecto</Button>
                    {selectProject ? <Button danger onClick={()=>{                        
                        setSelectClient(null)
                        form.resetFields()
                    }}>Cancelar</Button>:<Button onClick={()=>form.resetFields()} >Limpiar</Button>}
                    
                </Form.Item>
                
            </Form>}
        </Card>
    </>)

}


export default FormProject