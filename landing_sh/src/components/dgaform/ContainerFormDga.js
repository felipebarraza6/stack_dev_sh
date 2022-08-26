import React, { useState } from 'react'
import { Menu, Row, Col, Form, Tag,
          Radio, Input, Select, Cascader,
          InputNumber, Switch, Button,
          DatePicker, TreeSelect, Card, Typography,
          Affix } from 'antd'
import YourData from './YourData'
import Wells from './Wells'
import slidde from '../../assets/images/slide2.png'
import FormClientExternal from '../external_clients/FormClientExternal'

const ContainerFormDga = () => {

  const [selectKey, setSelectKey] = useState('1')
  const [wells, setWells] = useState(null)
  const [dataClient, setDataClient] = useState(null)
  const [quotation, setQuotation] = useState(null)

  const date = new Date()


  return(<>
          <Col span={12} style={styles.col_header}>
            <Typography.Title level={5}>
              COTIZACIÓN EXTERNA: {dataClient && <>{dataClient.data.name_enterprise}</>}
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
                  <FormClientExternal is_public={true} setSteps={setSelectKey} setQuotation={setQuotation} setDataClient={setDataClient} />
                </Col>
                  {dataClient ? 
                      
                        <Wells quantity={wells} setQuantity={setWells} quotation={quotation} />
                         :
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
