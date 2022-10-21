import React, { useState, useEffect } from 'react'
import { Row, Col, Card, Typography } from 'antd'
import Wells from './Wells'
import slidde from '../../assets/images/slide2.png'
import FormClientExternal from '../external_clients/FormClientExternal'
import { callbacks } from '../../api/endpoints'



const ContainerFormDga = ({ match }) => {

  const [wells, setWells] = useState(null)
  const [dataClient, setDataClient] = useState(null)
  const [quotation, setQuotation] = useState(null)
  const [listWells, setListWells] = useState(null)
  const date = new Date()

  
  async function getQuotation(uuid){
    const rq = await callbacks.quotation.retrieve(uuid).then((response)=> {
      setDataClient({data:response.data.external_client})
      setQuotation(response.data.uuid)
      setWells(response.data.wells.length)
      setListWells(response.data.wells)
    })
    return rq
  }


  useEffect(() => {
    if(match){
      getQuotation(match.params.id)
    }
  }, [])



  return(<>
          <Col span={12} style={styles.col_header}>
              <Typography.Title level={5}>
                 {dataClient ? <>COTIZACIÓN EXTERNA: {dataClient.data.name_enterprise}</>:<>REGISTRA TUS DATOS EN EL FORMULARIO</>}
              </Typography.Title>
            </Col>
            <Col span={12} style={styles.col_header}>
              <Typography.Title level={5} style={styles.title_date}>
                FECHA: {date.getDate()} - {<>{date.getMonth() < 10 ? <>0{date.getMonth()}</>:<>{date.getMonth()}</>}</>} - {date.getFullYear()}
              </Typography.Title>
            </Col>
            <Col span={24}>
            <Row style={styles.row}>              
                  <Col lg={6} xl={6} xs={24} style={{paddingTop:'20px', paddingRight:'10px', paddingLeft:'20px'}}>
                    {dataClient ? <Card>
                       <b>NOMBRE EMPRESA:</b><br/>{dataClient.data.name_enterprise}<br />
                       <b>NOMBRE CONTACTO:</b><br/>{dataClient.data.name_contact}<br/>
                       <b>EMAIL CONTACTO:</b><br/>{dataClient.data.mail_contact}<br/>
                       <b>TELEFONO CONTACTO:</b><br/>{dataClient.data.phone_contact}
                    </Card>: 
                  <FormClientExternal dataClient={dataClient} setQuotation={setQuotation} setDataClient={setDataClient} />
                    }
                </Col>
                  {dataClient ? <>
                          <Wells quantity={wells} listWellsArr={listWells} setQuantity={setWells} quotation={quotation} />:
                         </>:
                      <Col xs={24} lg={18} xl={18} style={{padding:'50px'}}>
                        <div style={{marginLeft:'0px', marginTop:'00px'}}>
                          <Typography.Title level={2}>DEBES RELLENAR TUS DATOS PARA CONTINUAR...</Typography.Title>
                          <img src={slidde} style={{width:'100%'}} />
                      </div>
                      </Col>
                  }      
      </Row></Col>
  </>)

}

const styles = {
  col_header: {
    padding:'20px',
    backgroundColor: 'white'
  },
  row: {
    Bottom:'20px',
  }, 
  
  title_date: {
    float: 'right',
  },
  col_datas: {
    padding:'20px',
  },

  }


export default ContainerFormDga
