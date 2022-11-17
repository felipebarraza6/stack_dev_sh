import React, { useState, useEffect } from 'react'
import  api from '../../api/endpoints'
import { Table, Button, Modal, 
          Tooltip, Card, Descriptions,
          Row, Col, Tag } from 'antd'
import { SendOutlined, CloudDownloadOutlined, EyeFilled } from '@ant-design/icons'

const Home = () => {

    const [listQuotations, setListQuotations] = useState([])
    
    async function getData(){
      const rq = await api.quotation.list().then((x)=> {        
        setListQuotations(x.data.results)
      })
      return rq
    }
    
    function modalRetrieveClient(client) {
      Modal.info({ 
        width: 750,
        okText: 'Volver',
        title: client.name_enterprise,
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
                  <Descriptions.Item label='Nombre empresa' span={3}>
                    <b>{client.name_enterprise}</b>
                  </Descriptions.Item>
          </Descriptions>
      })
    }
    
    function modalDataWells(wells) {
      Modal.info({
        width: 1000,  
        icon:<></>,    
        okText:'Volver',  
        content: <Row>
          {wells.map((x)=> {
            return(<Col span={12}><Card title={x.name}>
                <Descriptions bordered title={x.exact_address}>
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
            title: 'Datos de contacto',
            render: (x)=> <>
              {x.external_client.name_enterprise.length < 8 ? 
               <Button 
               type='primary'
               ghost
               style={{textAlign:'left'}}
               block
               icon={<EyeFilled style={{marginRight:'5px'}} />}
               onClick={()=>modalRetrieveClient(x.external_client)}>
                  {x.external_client.name_enterprise}                                 
             </Button>:<Tooltip color={'#f50'} title={x.external_client.name_enterprise}><Button 
               type='primary'
               ghost
               style={{textAlign:'left'}}
               block
               icon={<EyeFilled style={{marginRight:'5px'}} />}
               onClick={()=>modalRetrieveClient(x.external_client)}>
                  {x.external_client.name_enterprise.slice(0,20)}...                                 
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
          {            
            render: (x)=> {
              if(x.is_approved){
                return(<Button  danger>CANCELAR APROBACIÓN</Button>)
              } else {
                return(<>
                  <Button type='primary' icon={<SendOutlined />}>Revisado / Cotizar</Button>
                  <Button type='primary' icon={<CloudDownloadOutlined/>} style={{backgroundColor:'#389e0d', borderColor:'#389e0d', marginLeft:'10px'}}>Descargar reporte</Button>                  
                  </>)
              }
            }
          }
        ]}
        dataSource={listQuotations}></Table>)
}


export default Home
