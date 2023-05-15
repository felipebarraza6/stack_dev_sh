import React, { useState, useEffect } from 'react'
import  api from '../../api/endpoints'
import { Table, Button, Modal, 
          Tooltip, Card, Descriptions,
          Row, Col, Tag } from 'antd'
import { UserOutlined, BuildOutlined, CloudDownloadOutlined, EyeFilled, FileImageFilled } from '@ant-design/icons'

const InternalLifting = () => {

    const [listQuotations, setListQuotations] = useState([])
    
    async function getData(){
      const rq = await api.quotation.listf().then((x)=> {
        console.log(x)
        setListQuotations(x.data.results)
      })
      return rq
    }
    
    function modalRetrieveClient(client) {
      Modal.info({ 
        width: 750,
        okText: 'Volver',
        title: client.name_enterprise,
        icon: <UserOutlined />,
        content: <Descriptions bordered layout='horizontal' style={{marginTop:'50px'}} size='middle'>
                  <Descriptions.Item label='Nombre contacto' span={3}>
                    <b>{client.name_contact}</b>
                  </Descriptions.Item>            
                  <Descriptions.Item label='Teléfono' span={3}>
                    <b>{client.phone_contact}</b>
                  </Descriptions.Item>
                  <Descriptions.Item label='Email' span={3}>
                    <b>{client.mail_contact}</b>
                  </Descriptions.Item>                  
          </Descriptions>
      })
    }

    function modalRetrieveEnterprise(client) {
        Modal.info({ 
          width: 750,
          style: {top:0},
          icon: <BuildOutlined />,
          okText: 'Volver',
          title: client.name,
          content: <Descriptions bordered layout='horizontal' style={{marginTop:'50px'}} size='middle'>
                    <Descriptions.Item label='Nombre' span={3}>
                      <b>{client.name}</b>
                    </Descriptions.Item>            
                    <Descriptions.Item label='Teléfono' span={3}>
                      <b>{client.phone_number}</b>
                    </Descriptions.Item>
                    <Descriptions.Item label='Email' span={3}>
                      <b>{client.email}</b>
                    </Descriptions.Item>                  
                    <Descriptions.Item label='Region' span={3}>
                      <b>{client.region}</b>
                    </Descriptions.Item> 
                    <Descriptions.Item label='Comuna' span={3}>
                      <b>{client.commune}</b>
                    </Descriptions.Item> 
                    <Descriptions.Item label='Provincia' span={3}>
                      <b>{client.province}</b>
                    </Descriptions.Item> 
                    <Descriptions.Item label='Direccion' span={3}>
                      <b>{client.address_exact}</b>
                    </Descriptions.Item> 
                    <Descriptions.Item label='Cantidad de pozos' span={3}>
                      <b>{client.amount_regularized}</b>
                    </Descriptions.Item> 
                    <Descriptions.Item label='Cantidad de pozos regularizados' span={3}>
                      <b>{client.flow_rates}</b>
                    </Descriptions.Item>
            </Descriptions>
        })
      }
    
    function modalDataWells(wells) {
      Modal.info({
        width: '100%',  
        icon:<></>,    
        style:{top:0},
        okText:'Volver',  
        content: <Row justify='center' align='middle'>
          {wells.map((x)=> {
            return(<Col span={8}><Card title={x.name} style={{border:'1px solid black', borderRadius:'10px', marginRight:'10px'}}>
                {x.img1 && <Button icon={<FileImageFilled/>} type='primary' style={{margin:'5px'}} onClick={()=>window.open(`https://api.smarthydro.cl${x.img1}`)}>General</Button>}
                {x.img2 && <Button icon={<FileImageFilled/>}  type='primary' style={{margin:'5px'}} onClick={()=>window.open(`https://api.smarthydro.cl${x.img2}`)} >Detalle salida pozo</Button>}

                <Descriptions bordered size='small' title={x.exact_address}>
                  <Descriptions.Item span={3} label={<>Caudal otorgado <Tag color='geekblue'>(Lt/SEG)</Tag></>}>
                    {parseFloat(x.granted_flow).toFixed(2)}
                  </Descriptions.Item>
                  <Descriptions.Item span={3} label={<>Profundida total del pozo <Tag color='geekblue'>(Mt)</Tag></>}>
                    {parseFloat(x.well_depth).toFixed(2)}
                  </Descriptions.Item>
                  <Descriptions.Item span={3} label={<>Nivel estático <Tag color='geekblue'>(Mt)</Tag></>}>
                    {parseFloat(x.static_level).toFixed(2)}
                  </Descriptions.Item>
                  <Descriptions.Item span={3} label={<>Nivel dinámico <Tag color='geekblue'>(Mt)</Tag></>}>
                    {parseFloat(x.dynamic_level).toFixed(2)}
                  </Descriptions.Item>
                  <Descriptions.Item span={3} label={<>Profundida instalación bomba <Tag color='geekblue'>(Mt)</Tag></>}>
                    {parseFloat(x.pump_installation_depth).toFixed(2)}
                  </Descriptions.Item>
                  <Descriptions.Item span={3} label={<>Diámetro interior pozo <Tag color='geekblue'>(MM/PULG)</Tag></>}>
                    {parseFloat(x.inside_diameter_well).toFixed(2)}
                  </Descriptions.Item>
                  <Descriptions.Item span={3} label={<>Diámetro exterior ducto salida bomba <Tag color='geekblue'>(MM/PULG)</Tag></>}>
                    {parseFloat(x.duct_outside_diameter).toFixed(2)}
                  </Descriptions.Item>
                  <Descriptions.Item span={3} label={<>Cuenta con flujometro? </>}>
                    {x.has_flow_sensor}
                  </Descriptions.Item>                  
                </Descriptions>
              </Card></Col>)
          })}
        </Row>
      })
    }


    useEffect(() => {
      getData()
    }, [])

    return(<Table bordered
        columns = {[          
            {
                title: 'Cliente',
                render: (x)=> <>
                {x.client && <>
                  {x.client  ? 
                   <Button 
                   type='primary'
                   ghost
                   style={{textAlign:'left'}}
                   block
                   icon={<EyeFilled style={{marginRight:'5px'}} />}
                   onClick={()=>modalRetrieveEnterprise(x.client)}>
                      {x.client.id}                                 
                 </Button>:<Tooltip color={'#f50'} title={x.client.name}><Button 
                   type='primary'
                   ghost
                   style={{textAlign:'left'}}
                   block
                   icon={<EyeFilled style={{marginRight:'5px'}} />}
                   onClick={()=>modalRetrieveEnterprise(x.client)}>
                      {x.client.name.slice(0,20)}...                                 
                 </Button></Tooltip>
                  }</>}               
                </>
              },
          {
            title: 'Receptor de visita',
            render: (x)=> <>
              {x.external_client.name_contact.length < 8 ? 
               <Button 
               type='primary'
               ghost
               style={{textAlign:'left'}}
               block
               icon={<EyeFilled style={{marginRight:'5px'}} />}
               onClick={()=>modalRetrieveClient(x.external_client)}>
                  {x.external_client.name_contact}                                 
             </Button>:<Tooltip color={'#f50'} title={x.external_client.name_contact}><Button 
               type='primary'
               ghost
               style={{textAlign:'left'}}
               block
               icon={<EyeFilled style={{marginRight:'5px'}} />}
               onClick={()=>modalRetrieveClient(x.external_client)}>
                  {x.external_client.name_contact.slice(0,20)}...                                 
             </Button></Tooltip>
              }               
            </>
          },
          {
            title: 'Pozos',
            render: (x) => <>
              <Button 
                type='primary'
                ghost
                block
                icon={<EyeFilled />}
                onClick={()=> modalDataWells(x.wells)}>
                 {x.wells.length} {x.wells.length === 1 ? 'Pozo':'Pozos'}
              </Button>
            </>
          },
          {
            title: 'Fecha creación',
            render: (x) => {
              var date = new Date(x.created)
              var options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric', hour:'numeric', minute:'numeric' }
             return (<>{date.toLocaleDateString('es-ES', options).toUpperCase()}</>)
            }
          },                    
        ]}
        dataSource={listQuotations}></Table>)
}


export default InternalLifting
