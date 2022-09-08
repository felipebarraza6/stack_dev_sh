import React, { useState } from 'react'
import { Drawer, Form, Input, 
          Button, List, Card,
          Tag, Row, Col,
          Typography } from 'antd'

const DrawerSupport = ({ is_create, is_open, setStateNavigate, tickets }) => {
  
  const [form] = Form.useForm()
  const [drawerChild, setDrawerChild] = useState({
    visible: false,
    answers: [],
    ticket: {}
  })

  function onClose(){
    setStateNavigate(false)
  }

  function onCloseChildren(){
    setDrawerChild({
      ...drawerChild,
      visible: false  
    })
  }

  function resetForm(){
    form.resetFields()
  }

  const Ticket = (ticket) => <List.Item>
      <DrawerComments  />
      <Card hoverable 
        title={<>
          {ticket.created.slice(0,10)} 
        </>} 
        extra={<><Tag color={'geekblue'}>
           {ticket.created.slice(11,19)}
          </Tag>
          <Tag>
            ID: #{ticket.id}
          </Tag>
          </>} 
        >
        <Row>
          <Col span={12}>
            <Typography.Paragraph>{ticket.affair}</Typography.Paragraph>
          </Col>
          <Col span={12} align={'end'}>
            <Button type={'primary'} onClick={()=> {
              setDrawerChild({
                ...drawerChild, 
                visible:true,
                ticket: ticket,
                answers: ticket.answers
              })}}>Ver comentarios ({ticket.answers.length})</Button>
          </Col>
        </Row>
      </Card>
    </List.Item>

    const DrawerComments = () => {

      const [form] = Form.useForm()

      return(<Drawer width={450} title={`Comentarios ticket: #${drawerChild.ticket.id}`} 
                visible={drawerChild.visible}
                onClose={onCloseChildren}>
            {drawerChild.answers.length > 0 ? 
            <List>
              {drawerChild.answers.map((obj)=>{
                return(<>
                  {obj.is_admin_answer ? 
                  <Card title={<Tag color={'geekblue'}>{obj.administrator.first_name} - ADMINISTRADOR</Tag>}
                    style={{borderRadius:'10px', marginTop:'10px', marginBottom: '10px', backgroundColor:'#1890ff', color:'white'}}
                    extra={<div style={{color:'white'}}>{obj.created.slice(0,10)} / {obj.created.slice(11,16)}</div>}>
                    <Typography.Paragraph style={{color:'white'}}>{obj.answer}</Typography.Paragraph>
                  </Card>: <Card title={'YO'} 
                    extra={`${obj.created.slice(0,10)} / ${obj.created.slice(11,16)}`}
                    style={{marginLeft:'20px', marginTop:'10px', marginBottom: '10px'}}>
                    <Typography.Paragraph>{obj.answer}</Typography.Paragraph>
                  </Card>}
                </>) 
              })}
                <Form form={form}>
                  <Form.Item name='answer'>
                    <Input.TextArea rows={4} placeholder={'ESCRIBE TU RESPUESTA'} />
                  </Form.Item>
                  <Form.Item style={{marginTop:'-20px'}} >
                    <Button type={'primary'} size={'small'}>ENVÍAR</Button>
                    <Button size={'small'} onClick={()=> form.resetFields()} style={{marginLeft:'10px'}}>LIMPIAR</Button>
                  </Form.Item>
                </Form>
            </List>:
            <Typography.Title level={3}>SIN COMENTARIOS AÚN...</Typography.Title>}
        </Drawer>)
    }


  return(<Drawer title={is_create ? 'Crear Ticket': 'Tickets'} 
          onClose={onClose} 
          visible={is_open} 
          open={DrawerComments}
          width={500} >
      {is_create ? 
        <Form layout={'vertical'} form={form}>
          <Form.Item label='MENSAJE' name='affair'>
            <Input.TextArea rows={10} placeholder={'DESCRIBE TU PROBLEMA EN RELACIÓN AL MODULO ACTUAL...'}>
            </Input.TextArea>
          </Form.Item>
          <Form.Item>
            <Button type='primary' style={styles.button}>ENVÍAR</Button>
            <Button style={styles.button} onClick={resetForm}>LIMPIAR</Button>
          </Form.Item>
        </Form>:<>{tickets && <List grid={{ gutter: 16, column: 4 }}>
            {tickets.map((ticket)=> <Ticket {...ticket} />)}
          </List>}
        </>
      }
    </Drawer>)
}

const styles = {
  button: {
    margin: '10px'
  }
}


export default DrawerSupport
