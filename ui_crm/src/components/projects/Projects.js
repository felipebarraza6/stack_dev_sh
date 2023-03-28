import React, {useState} from 'react'
import { Row, Col, Typography, 
          Card, Input, Button,
          Table, Select, Descriptions, Modal, Drawer } from 'antd'

const { Title } = Typography

const Projects = () => {

  const [open, setOpen] = useState(false)

  return(<Row>
          <Col span={24}>
            <Title>Proyectos</Title>
          </Col>
          <Col span={10}>

          <Drawer visible={open} onClose={()=>setOpen(false)} title='P1' width={'600px'}>
              <Descriptions title='Nombre pozo'>
                <Descriptions.Item>Caudal otorgado</Descriptions.Item>
                <Descriptions.Item>Profundidad del pozo</Descriptions.Item>
                <Descriptions.Item>Nivel estatico</Descriptions.Item>
                <Descriptions.Item>Nivel dinamico</Descriptions.Item>
                <Descriptions.Item>Profundidad de instalacion</Descriptions.Item>
                <Descriptions.Item>Diametro interior pozo</Descriptions.Item>
                <Descriptions.Item>Diamtro exterior del ducto</Descriptions.Item>
                <Descriptions.Item>Cuenta con sensor de flujo?</Descriptions.Item>
                <Descriptions.Item>Ubicacion</Descriptions.Item>
                <Descriptions.Item>Imagenes</Descriptions.Item>
                <Descriptions.Item>Tipo captacion</Descriptions.Item>
                <Descriptions.Item>Persona a cargo</Descriptions.Item>
              </Descriptions>
<Descriptions title='Datos resolución'>
                      <Descriptions.Item>
                        Nro resolución
                    </Descriptions.Item>
                    <Descriptions.Item>Sector hidrologico(SHAC))</Descriptions.Item>
                    <Descriptions.Item>Fecha publicación diario</Descriptions.Item>
                    <Descriptions.Item>Plazo instalación</Descriptions.Item>
                    <Descriptions.Item>Plazo transmisión</Descriptions.Item>
                    <Descriptions.Item>Estandar</Descriptions.Item>

                    </Descriptions>
<Descriptions title='Encargado pozo'>
                      <Descriptions.Item>Nombre</Descriptions.Item>
                    <Descriptions.Item>Correo</Descriptions.Item>
                    <Descriptions.Item>Telefono</Descriptions.Item>
                    <Descriptions.Item>Cargo</Descriptions.Item>

                    </Descriptions>




    </Drawer>
            <Card title='Resumen proyecto'>
              <Descriptions bordered layout='vertical'>
                <Descriptions.Item span={2} label='Codigo'>#1234</Descriptions.Item>
                <Descriptions.Item label='Cliente'><Button onClick={()=>Modal.info({width:'700px', title:'Información general', content: <>
<Descriptions title='Nombre cliente'>
                      <Descriptions.Item>
                      Nombre
                    </Descriptions.Item>
                    <Descriptions.Item>Rut</Descriptions.Item>
                    <Descriptions.Item>Telefono</Descriptions.Item>
                    <Descriptions.Item>Region</Descriptions.Item>
                    <Descriptions.Item>Comuna</Descriptions.Item>
                    <Descriptions.Item>Provincia</Descriptions.Item>

                    <Descriptions.Item>Direccion</Descriptions.Item>

                    <Descriptions.Item>Cantidad de pozo</Descriptions.Item>

                    <Descriptions.Item>Pozos regualarizados</Descriptions.Item>

                    <Descriptions.Item>Acitivadad economica</Descriptions.Item>

                    </Descriptions>



                  </>})} type='primary' size='small'>Nombre cliente</Button></Descriptions.Item>
                <Descriptions.Item span={3} label='Fichas de levantamiento'>
                  <Button type='primary' >Crear ficha +</Button>
                  <Button onClick={()=>Modal.info({content:<>
                      <Descriptions title='General'>
                      <Descriptions.Item>Nombre cliente</Descriptions.Item>
                    <Descriptions.Item>Correo</Descriptions.Item>
                    <Descriptions.Item>Telefono</Descriptions.Item>
                    <Descriptions.Item>Rut</Descriptions.Item>
                    <Descriptions.Item>Dirección</Descriptions.Item>

                    <Descriptions.Item>Región y comuna</Descriptions.Item>
                    </Descriptions>
                      <Descriptions title='Pozos'> 
                        <Descriptions.Item>
                        <Button onClick={()=>setOpen(true)}>P1</Button><Button>P2</Button>

                        </Descriptions.Item>
                        </Descriptions>
<Descriptions title='Contacto empresa'>
                      <Descriptions.Item>Nombre</Descriptions.Item>
                    <Descriptions.Item>Correo</Descriptions.Item>
                    <Descriptions.Item>Telefono</Descriptions.Item>
                    <Descriptions.Item>Cargo</Descriptions.Item>

                    </Descriptions>


                                          </>, width:'600px',title:'Ficha1'})}>#1</Button>
                  <Button>#2</Button>
                  <Button>#3</Button>
                  <Button>#4</Button>
                  <Button>#5</Button>
                </Descriptions.Item>
                <Descriptions.Item label='Archivos'>
                  <Button size='small' onClick={()=>Modal.info({ title:'Cotizaciones',content:<>
                  <Button style={{margin:'10px'}} type='dashed'>Archivo1</Button>
<Button style={{margin:'10px'}} type='dashed'>Archivo2</Button>
<Button style={{margin:'10px'}} type='dashed'>Archivo3</Button>
<Button style={{margin:'10px'}} type='dashed'>Archivo4</Button>
                    </>})} style={{backgroundColor:'#3f6600', color:'white'}}>Cotizaciones</Button>
                  <Button size='small' style={{backgroundColor:'#613400', color:'white'}}>Ordenes de compra</Button>
                  <Button size='small' style={{backgroundColor:'#030852', color:'white'}}>Facturas</Button>
                  <Button size='small' style={{backgroundColor:'#520339', color:'white'}}>Programación</Button>
                  <Button size='small' style={{backgroundColor:'#002329', color:'white'}}>Informes técnicos</Button>
                </Descriptions.Item>

              </Descriptions>
            </Card>
          </Col>
          <Col span={8}>
            <Card title='Proyectos'>
              <Select placeholder='Filtrar por cliente...' style={{width:'100%'}}>
<Select.Option>Cliente</Select.Option>
                <Select.Option>Cliente</Select.Option>
                <Select.Option>Cliente</Select.Option>
                <Select.Option>Cliente</Select.Option>
                <Select.Option>Cliente</Select.Option>

    </Select>
              <Table columns={[{title:'Codigo', dataIndex:'code'}, {title:'Cliente',dataIndex:'client'}, {render:()=><Button size='small'type='primary'>Ver proyecto</Button>}]} dataSource={[{
                'code':'123', 'client':'Nombre cliente' 
              }]} />
            </Card>
          </Col>
          <Col span={6}>
            <Card title='Crear'>
              <Input placeholder='Nombre proyecto' style={{marginBottom:'10px'}} />
              <Input placeholder='Codigo proyecto' style={{marginBottom:'10px'}}/>
              <Select placeholder='Cliente' style={{width:'100%', marginBottom:'10px'}}>
                <Select.Option>Cliente</Select.Option>
                <Select.Option>Cliente</Select.Option>
                <Select.Option>Cliente</Select.Option>
                <Select.Option>Cliente</Select.Option>
                <Select.Option>Cliente</Select.Option>
              </Select>
              <Button type='primary' block>Crear</Button>
            </Card>
          </Col>
    </Row>)
}


export default Projects
