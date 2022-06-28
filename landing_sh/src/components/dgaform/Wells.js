import React, { useState } from 'react'
import { Col, Row, Card,
        Tag, Button, Input, List, 
        Menu, Typography, Badge } from 'antd'

import img_pozo from '../../assets/images/dem1.png'

const Wells = ({ quantity, setQuantity }) => {
      
    const [addWell, setAddWell] = useState(false)
    const [listWells, addListWells] = useState([])
    const [inputName, setInputName] = useState('')
    const [inputType, setInputType] = useState('')
    const [key, setKey] = useState('0')
    
          return(<Row>
                <Col style={styles.col_datas}>
                  <Card title={<>{quantity ? quantity:'0'} POZOS INGRESADOS</>} bordered hoverable>
                    <Row>
                      <Col>
                         <Button type='primary' onClick = {()=> setAddWell(true)}>AGREGAR POZO (+)</Button><br /><br />
                         {addWell && <>
                           Nombre o sector del pozo: <br/><Input onChange={(e)=>setInputName(e.target.value)} size="small" style={{width:'140px'}} /><br />
                           Tipo captación: <br />
                           <Input onChange={(e)=>setInputType(e.target.value)} size="small" style={{width:'140px'}} /><br />
                          <Button type='primary' style={{marginTop:'10px'}} onClick = {()=> {
                            addListWells([...listWells, {name:inputName, type: inputType}])
                            setInputName('')
                            setInputType('')
                            setAddWell(false)
                            setQuantity(quantity+1)
                          }}>CARGAR POZO</Button>
                         </>}
                      </Col>
                    </Row> 
                  </Card>
                </Col>
                <Col style={styles.col_datas}>
                  <Card style={{width:'800px'}}>
                    <Row>
                      <Col span={24}>
                        <Menu mode="horizontal" onClick={(x)=> setKey(x.key)}>
                          {listWells.map((x, index)=> <Menu.Item key={index}>{x.name}</Menu.Item>)}
                        </Menu>
                        {listWells.length > 0 && <>
                          <Row>
                            <Col span={12}>
                              <List bordered style={{marginTop:'20px'}}>
                                  <List.Item>1 - Caudal otorgado: <Tag color='blue'>LTRS/SEG</Tag></List.Item>
                                  <List.Item>2 - Profundidad: <Tag color='blue'>MTRS</Tag></List.Item>
                                  <List.Item>3 - Nivel Estatico: <Tag color='blue'>MTRS</Tag></List.Item>
                                  <List.Item>4 - Nivel Dinamico: <Tag color='blue'>MTRS</Tag></List.Item>
                                  <List.Item>5 - Profundidad instalacion bomda: <Tag color='blue'>MTRS</Tag></List.Item>
                                  <List.Item>6 - Diametro interior pozo: <Tag color='blue'>MM/P</Tag></List.Item>
                                  <List.Item>7 - Diametro exterior ducto: <Tag color='blue'>MM/P</Tag></List.Item>
                              </List>
                            </Col>
                            <Col span={12} style={styles.col_well}>
                                <Input style={{...styles.input, marginTop:'70px', marginLeft:'30px'}} prefix={<Badge count={1} style={styles.badgeNumber} />} />
                                <Input style={{...styles.input, marginTop:'230px', marginLeft:'80px'}} prefix={<Badge count={2} style={styles.badgeNumber} />} />
                                <Input style={{...styles.input, marginTop:'180px', marginLeft:'240px'}} prefix={<Badge count={3} style={styles.badgeNumber} />} />
                                <Input style={{...styles.input, marginLeft:'248px', marginTop:'240px'}} prefix={<Badge count={4} style={styles.badgeNumber} />} />
                                <Input style={{...styles.input, marginTop:'290px', marginLeft:'230px'}} prefix={<Badge count={5} style={styles.badgeNumber} />} />
                                <Input style={{...styles.input, marginTop:'130px', marginLeft:'240px'}} prefix={<Badge count={6} style={styles.badgeNumber} />} />
                                <Input style={{...styles.input, marginTop:'80px', marginLeft:'180px'}} prefix={<Badge count={7} style={styles.badgeNumber} />} />
                            </Col>
                          </Row>
                        </>}
                      </Col>
                    </Row> 
                  </Card>
                </Col>

          </Row>)
}


const styles = {
  col_well: {
    backgroundImage: `url(${img_pozo})`,
    backgroundPosition: 'center',
    backgroundSize: '180% auto',
                                          height: '400px',
                                          backgroundRepeat: 'no-repeat',
                                          width: '100%'
  },
  input: {
    position: 'absolute',
    width: '30%',
  },
  badgeNumber: {
    backgroundColor: '#1890ff',
  },
  img_well:{
    backgroundImage: `url${img_pozo}`,
    backgroundPosition: 'center',
    backgroundSize: '100% auto',
    height: '300px',
    width: '100%',
    backgroundRepeat: 'no-repeat',
    marginTop: '100px',
  },
  col_datas: {
    padding:'20px',
  },
  col_datas_b: {
    paddingleft: '20px',
    paddingright: '20px',
    marginbottom: '100px',
  },
  col_tech: {
    padding: '3px'
  }, 
  tag: {
    margin: '3px'
  }
}


export default Wells
