import React, {useEffect, useState} from 'react'
import { Row,Col, Typography, Input } from 'antd'
import Navigate from './Navigate'
import StatusLine from './StatusLine'
import {callbacks} from '../../api/endpoints'


const Init = ({match}) => {

  const initialState = {
    id_fingerprint: match.params.id,
    data_fingerprint: null
  }

  const [state, setState] = useState(initialState)

  const getData = async()=> {
    const rq = await callbacks.fingerprint.retrieve(state.id_fingerprint).then((x)=> console.log(x))
  }

  useEffect(()=> {
    getData()

  }, [])


    return(<>
      <Col span={6} style={styles.container}>
        <Typography.Title level={4}>HUELLA HÍDRRICA</Typography.Title>
        <Navigate />
      </Col>

      <Col span={18} style={styles.nav}>
        <StatusLine />
        <Row style={{marginTop:'20px'}}>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 1"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 2"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 3"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 4"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 5"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 6"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 7"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 8"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 9"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 10"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 11"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 12"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 13"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 14"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 15"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 16"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 17"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 18"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 19"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 20"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 21"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 22"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 23"/>
          </Col>
          <Col style={{padding:'10px'}}>
            <Input placeholder="CAMPO 24"/>
          </Col>
        </Row>
      </Col>
    </>)
}

const styles = {
  container: {
    padding: '20px'
  },
  nav:{
    backgroundColor: 'white',
    padding: '20px'
  },
}

export default Init
