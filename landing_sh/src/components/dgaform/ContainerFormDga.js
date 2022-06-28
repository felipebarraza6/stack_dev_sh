import React, { useState } from 'react'
import { Menu, Row, Col, Form, Tag,
          Radio, Input, Select, Cascader,
          InputNumber, Switch, Button,
          DatePicker, TreeSelect, Card, Typography,
          Affix } from 'antd'
import YourData from './YourData'
import Wells from './Wells'

const ContainerFormDga = () => {

  const [selectKey, setSelectKey] = useState('1')
  const [wells, setWells] = useState(null)

  const date = new Date()

  const [data, setData] = useState({
    general: {
      name: 'Smart Hydro',
      region: 'Región de Ñuble',
      commune: 'Chillán'
    },
    contact: {
      name: 'Diego Mardones',
      mail: 'diegomardones@smarthydro.cl',
      phone: '+56 9 8714 0109'
    },
    technicians: {
      resolution: 'N°182',
      standard: 'MAYOR',
      date_installation: '08-2020',
      date_transmission: '09-2020',
      date_diary_official: '03-2020'
    }
  })


  return(<>
          <Col span={12} style={styles.col_header}>
            <Typography.Title level={5}>
              UUID: AAAA-AAAA-AAAA-AAAA
            </Typography.Title>
          </Col>
          <Col span={12} style={styles.col_header}>
            <Typography.Title level={5} style={styles.title_date}>
              FECHA: {date.getDate()} - {<>{date.getMonth() < 10 ? <>0{date.getMonth()}</>:<>{date.getMonth()}</>}</>} - {date.getFullYear()}
            </Typography.Title>
          </Col>
          <Row style={styles.row}>
            <Col style={styles.col_datas}>
              <Affix>
                <Menu mode='inline' theme='dark' onClick={(x)=>setSelectKey(x.key)} defaultSelectedKeys={['1']}>
                  <Menu.Item key='1'>TUS DATOS</Menu.Item>
                  <Menu.Item key='2'>POZOS({wells ? wells: '0'})</Menu.Item>
                  <Menu.Item key='3'>PREVISUALIZACION</Menu.Item>
                  <Menu.Item key='4'>FINALIZAR</Menu.Item>
                </Menu>
              </Affix>
            </Col>
              {selectKey === '1' && <>
                  <YourData data={data} />
              </>}
              {selectKey === '2' && <>
                  <Wells quantity={wells} setQuantity={setWells} />
              </>}
    </Row>
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
