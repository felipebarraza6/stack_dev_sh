import React, { useState, useEffect } from 'react'
import  api from '../../api/endpoints'
import { Table, Button, Modal, 
          Typography, Card, Descriptions,
          Row, Col } from 'antd'
import { UserOutlined, UnorderedListOutlined } from '@ant-design/icons'

const Home = () => {

    const [listQuotations, setListQuotations] = useState([])
    
    async function getData(){
      const rq = await api.quotation.list().then((x)=> {
        console.log(x)
        setListQuotations(x.data.results)
      })
      return rq
    }
    
    function modalRetrieveClient(client) {
      Modal.info({ 
        width: 500,
        title: client.name_contact,
        content: <Typography.Paragraph>
                    <b>NOMBRE CONTACTO:</b> {client.name_contact}<br/>
                    <b>TELEFONO:</b> {client.phone_contact}<br/>
                    <b>CORREO:</b> {client.mail_contact}<br/>
                    <b>NOMBE EMPRESA:</b> {client.name_enterprise}<br/>
                    <b>DIRECCIÓN EMPRESA:</b> {client.address_enterprise}<br/>
          </Typography.Paragraph>
      })
    }
    
    function modalDataWells(wells) {
      Modal.info({
        width: 1000,
        title: 'POZOS',
        content: <Row>
          {wells.map((x)=> {
            return(<Col span={12}><Card title={x.name}>
                <Descriptions bordered>
                  <Descriptions.Item span={3} label='Caudal otorgado (Lt/SEG)'>{x.granted_flow}</Descriptions.Item>
                  <Descriptions.Item span={3} label='Profundida total del pozo (Mt)'>{x.well_depth}</Descriptions.Item>
                  <Descriptions.Item span={3} label='Nivel estático (Mt)'>{x.static_level}</Descriptions.Item>
                  <Descriptions.Item span={3} label='Nivel dinámico (Mt)'>{x.dynamic_level}</Descriptions.Item>
                  <Descriptions.Item span={3} label='Profundida instalación bomba (Mt)'>{x.pump_installation_depth}</Descriptions.Item>
                  <Descriptions.Item span={3} label='Diámetro interior pozo (MM/PULG)'>{x.inside_diameter_well}</Descriptions.Item>
                  <Descriptions.Item span={3} label='Diámetro exterior ducto salida bomba (MM/PULG)'>{x.duct_outside_diameter}</Descriptions.Item>
                </Descriptions>
              </Card></Col>)
          })}
        </Row>
      })
    }

    console.log(listQuotations)

    useEffect(() => {
      getData()
    }, [])

    return(<Table
        columns = {[
          {
            title:'URL Cotización',
            render: (x)=> <>
              <a href={`https://smarthydro.cl/dgaform/external_client/${x.uuid}`} target="_blank">{x.uuid}</a>
            </>
          }, 
          {
            title: 'Cliente',
            render: (x)=> <>
              <Button icon={<UserOutlined />}
                type='primary'
                onClick={()=>modalRetrieveClient(x.external_client)}>
                  {x.external_client.name_enterprise}
              </Button>
            </>
          },
          {
            title: 'POZOS',
            render: (x) => <>
              <Button icon={<UnorderedListOutlined />} type='primary'
                onClick={()=> modalDataWells(x.wells)}>
                POZOS({x.wells.length})
              </Button>
            </>
          },
          {
            title: 'Está aprobada?',
            render: (x)=> {
              if(x.is_approved){
                return(<Button  danger>CANCELAR APROBACIÓN</Button>)
              } else {
                return(<Button >APROBAR</Button>)
              }
            }
          }
        ]}
        dataSource={listQuotations}></Table>)
}


export default Home
