import React, { useState } from 'react'

import { Modal, Form, Input, Select, Alert } from 'antd'

const { Option } = Select

const ModalForm = ({visible, onCreate, onCancel, enterprise, error }) => {

    const [form] = Form.useForm()

    const [other, setOther] = useState({
      other_charge:false
    })
   
    return(
      <React.Fragment>
        <Modal
            visible={visible}
            title={enterprise ? `Nueva persona en ${enterprise.name}`: `Editar persona` }
            okText ="Guardar"
            cancelText="Cancelar"
            onCancel={onCancel}
            onOk={() => {
                form
                  .validateFields()
                  .then(values => {
                    form.resetFields();
                    onCreate(values);
                  })
                  .catch(info => {
                    console.log('Validate Failed:', info);
                  });
              }}
        >
          {error && <Alert style={{marginBottom:'5px'}} message="Error" description={error.email} type='error' />}
            <Form
            form={form}
            layout="vertical"
            name="FormPerson"            
            >
              <Form.Item name="name" label="Nombre" rules={[
                {
                  required:true,
                  message:'Porfavor ingresa el nombre'
                }
              ]}>
                <Input />

              </Form.Item>

            
              <Form.Item name="charge" label="Cargo" rules={[
                {
                  required:true,
                  message:'Porfavor ingresa el cargo'
                }
              ]}>
                {other.other_charge ? 
                  <Input placeholder="Escribe el cargo" />:
                  <Select name="charge" placeholder="Selecciona un cargo" onSelect={(value)=> {
                    if(value==='Otro Cargo'){
                      setOther({
                        other_charge:true                        
                      })
                      value = null
                    }
                  }} >                
                      <Option value="Gerente General">Gerente General</Option>
                      <Option value="Gerente de Operaciones">Gerente de Operaciones</Option>
                      <Option value="Jefe de Operaciones">Jefe de Operaciones</Option>
                      <Option value="Jefe de Planta">Jefe de Planta</Option>
                      <Option value="Jefe de Mantención">Jefe de Mantención</Option>
                      <Option value="Secretaria General">Secretaria General</Option>
                      <Option value="Secretaria administrativa">Secretaria administrativa</Option>
                      <Option value="Secretaria Gerencia">Secretaria Gerencia</Option>
                      <Option value="Otro Cargo">Otro</Option>
                  </Select>
                }
                

              </Form.Item>

              <Form.Item name="phone_number" label="Telefono" rules={[{ required: false, message: 'Ingresa el telefono'}]}>
                <Input name="phone_number" type="text" maxLength={9} />
              </Form.Item>

              <Form.Item name="email" label="Email" rules={[{ type:"email", required: true, message: 'Ingresa el correo electrónico'}]}>
                  <Input name="email" type="email" />
              </Form.Item>

            </Form>
        </Modal>
        </React.Fragment>
    )

}

export default ModalForm