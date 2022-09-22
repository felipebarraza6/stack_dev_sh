import React, { useState, useEffect } from 'react'
import { Col, Row, Card, Select,
        Tag, Button, Input, List, Spin, Modal,
        Menu, notification, Badge } from 'antd'
import { SmileTwoTone } from '@ant-design/icons'

import img_pozo from '../../assets/images/dem1.png'
import { callbacks } from '../../api/endpoints'

const Wells = ({ quantity, setQuantity, quotation, listWellsArr }) => {
      
    const [addWell, setAddWell] = useState(false)
    const [listWells, addListWells] = useState([])
    const [inputName, setInputName] = useState(null)
    const [selectCaptation, setSelectCaptation] = useState(null)    
    const [key, setKey] = useState('0')
    const [selectedWell, setSelectedWell] = useState({})
    const [loadWell, setLoadWell] = useState(false)
    const [dataSending, setDataSending] = useState(false)
    const [bloackedButton, setBlockedButton] = useState(true)

    async function sendData(){      
      var dataCompleted = true
      listWells.map((x)=> {
        if(x['duct_outside_diameter']==''){
          notification.error({
            message: 'DEBES COMPLETAR ESTE CAMPO', 
            description: `Diámetro exterior ducto, en el pozo ${x.name}`
          })
          dataCompleted = false
        }
        if(x['dynamic_level']==''){
          notification.error({
            message: 'DEBES COMPLETAR ESTE CAMPO', 
            description: `Nivel Dinámico, en el pozo ${x.name}`
          })
          dataCompleted = false
        }
        if(x['granted_flow']==''){
          notification.error({
            message: 'DEBES COMPLETAR ESTE CAMPO', 
            description: `Caudal otorgado, en el pozo ${x.name}`
          })
          dataCompleted = false
        }
        if(x['inside_diameter_well']==''){
          notification.error({
            message: 'DEBES COMPLETAR ESTE CAMPO', 
            description: `Diámetro interior pozo, en el pozo ${x.name}`
          })
          dataCompleted = false
        }
        if(x['pump_installation_depth']==''){
          notification.error({
            message: 'DEBES COMPLETAR ESTE CAMPO', 
            description: `Profundidad instalacion bomda, en el pozo ${x.name}`
          })
          dataCompleted = false
        }
        if(x['static_level']==''){
          notification.error({
            message: 'DEBES COMPLETAR ESTE CAMPO', 
            description: `Nivel Estático, en el pozo ${x.name}`
          })
          dataCompleted = false
        }
        if(x['well_depth']==''){
          notification.error({
            message: 'DEBES COMPLETAR ESTE CAMPO', 
            description: `Profundida total del pozo, en el pozo ${x.name}`
          })
          dataCompleted = false
        }       
      })
      if(dataCompleted){ 
      const rq = await callbacks.quotation.createWell(listWells).then((res)=> {        
        setDataSending(true)    
        setTimeout(() => { window.location.assign('/') }, 7000)
      })
      return rq
      }
    }

    useEffect(() => {
      if(listWellsArr){
        console.log(listWellsArr)
        addListWells(listWellsArr)
      }
    }, [])
    
          return(<>
            <Modal icon={SmileTwoTone} title='DATOS CARGADOS CORRECTAMENTE, GRACIAS POR LA INFORMACIÓN, TE ENVIAREMOS UNA COTIZACION A LA BREVEDAD...' 
              visible={dataSending}
                footer={[]}>
              <center><Spin size='large' /></center>
            </Modal>
            <Col style={{padding:'10px'}} sm={5} xl={5} lg={5} xs={24}>
                  <Card title={<>{quantity ? quantity:'0'} POZOS INGRESADOS</>} bordered hoverable>
                    <Row>
                      <Col>
                         <Button type='primary' onClick = {()=> setAddWell(true)}>AGREGAR POZO (+)</Button><br /><br />
                         {addWell && <>
                      Nombre o sector del pozo: <br /><Input onChange={(e) => {
                          if(e.target.value == ''){
                            setInputName(null) 
                          } else{
                            setInputName(e.target.value)
                          }                          
                          
                          }} size="small" style={{ width: '140px' }} /><br /><br />
                           Fuente de captación: <br/><Select onChange={(e)=> setSelectCaptation(e)} placeholder="Selecciona una opción...">
                              <Select.Option value="pozo">POZO</Select.Option>
                              <Select.Option value="puntera">PUNTERA</Select.Option>
                            </Select><br /><br />
                            <Button type='primary' style={{marginTop:'10px'}} onClick = {()=> {
                              if(inputName==null || selectCaptation==null){
                                notification.error({message:'DEBES INGRESAR LOS CAMPOS'})                                
                              } else{
                                setSelectedWell({
                                  name: inputName,
                                  type_captation: selectCaptation
                                })
                                addListWells([
                                  ...listWells,
                                  {
                                    name: inputName,
                                    quotation: quotation,
                                    granted_flow: '',
                                    type_captation: selectCaptation,
                                    well_depth: '',
                                    static_level: '',
                                    dynamic_level: '',
                                    pump_installation_depth: '',
                                    inside_diameter_well: '',
                                    duct_outside_diameter: ''
                                  }])
                                setAddWell(false)
                                setInputName(null)
                                setSelectCaptation(null)
                                setQuantity(quantity + 1)
                              }                                                        
                          }}>CARGAR POZO</Button>
                         </>
}

                      </Col>
                    </Row> 
                  </Card>
            </Col>             
            <Col style={{padding:'20px'}} xl={13} sm={13} lg={13} xs={24}>                  
                  <Card style={{width:'100%'}}>
                    <Row>
                      <Col span={24}>
                        <Menu mode="horizontal" onClick={(x)=> {
                            setKey(x.key) 
                            setSelectedWell(listWells[x.key]) 
                            setTimeout(()=> {
                              if(loadWell){
                                setLoadWell(false)
                              } else{
                                setLoadWell(true)
                                setLoadWell(false)
                              }
                            },500)
                        }}>
                          {listWells.map((x, index)=> <>
                            <Menu.Item key={index}>{x.name}</Menu.Item>
                            </>)}
                        </Menu>
                        {listWells.length > 0 && <>
                          <Row>
                            {loadWell ? <Spin />:<>
                            <Col lg={12} xs={24}>
                              <List bordered style={{marginTop:'20px'}}>
                                  <List.Item>1 - Caudal otorgado: <Tag color='blue'>Lt/SEG</Tag></List.Item>
                                  <List.Item>2 - Profundidad total del pozo: <Tag color='blue'>Mt</Tag></List.Item>
                                  <List.Item>3 - Nivel Estático: <Tag color='blue'>Mt</Tag></List.Item>
                                  <List.Item>4 - Nivel Dinámico: <Tag color='blue'>Mt</Tag></List.Item>
                                  <List.Item>5 - Profundidad instalacion bomda: <Tag color='blue'>Mt</Tag></List.Item>
                                  <List.Item>6 - Diámetro interior pozo: <Tag color='blue'>MM/PULG</Tag></List.Item>
                                  <List.Item>7 - Diámetro exterior ducto salida bomba: <Tag color='blue'>MM/PULG</Tag></List.Item>
                              </List>
                            </Col>                            
                            <Col lg={12} xs={24} style={styles.col_well}>
                              <Tag color={'geekblue'} style={{margin:'20px', position:'absolute'}}>{selectedWell.name}({selectedWell.type_captation})</Tag>
                                <Input style={{...styles.input, marginTop:'70px', marginLeft:'30px'}} prefix={<Badge count={1} style={styles.badgeNumber} />}
                                  defaultValue={selectedWell.granted_flow}                                  
                                  onChange = {(e)=> {
                                    listWells[key].granted_flow= e.target.value
                                  }}
                                />
                                <Input style={{...styles.input, marginTop:'230px', marginLeft:'80px'}} prefix={<Badge count={2} style={styles.badgeNumber} />} 
                                  defaultValue={selectedWell.well_depth}
                                  onChange = {(e)=> {
                                    listWells[key].well_depth= e.target.value
                                  }}
                                />
                                <Input style={{...styles.input, marginTop:'180px', marginLeft:'240px'}} prefix={<Badge count={3} style={styles.badgeNumber} />}
                                  defaultValue={selectedWell.static_level}                                  
                                  onChange = {(e)=> {
                                    listWells[key].static_level= e.target.value
                                  }}
/>
                                <Input style={{...styles.input, marginLeft:'248px', marginTop:'240px'}} prefix={<Badge count={4} style={styles.badgeNumber} />}
                                  defaultValue={selectedWell.dynamic_level}
                                  onChange = {(e)=> {
                                    listWells[key].dynamic_level= e.target.value
                                  }}
 />
                                <Input style={{...styles.input, marginTop:'290px', marginLeft:'230px'}} prefix={<Badge count={5} style={styles.badgeNumber} />}                                   defaultValue={selectedWell.pump_installation_depth}
                                  onChange = {(e)=> {
                                    listWells[key].pump_installation_depth= e.target.value
                                  }}
/>
                                <Input style={{...styles.input, marginTop:'130px', marginLeft:'240px'}} prefix={<Badge count={6} style={styles.badgeNumber} />}                                   
                                defaultValue={selectedWell.inside_diameter_well} 
                                onChange = {(e)=> {
                                    listWells[key].inside_diameter_well= e.target.value
                                  }}
 />
                                <Input style={{...styles.input, marginTop:'80px', marginLeft:'180px'}} prefix={<Badge count={7} style={styles.badgeNumber} />} 
                                   defaultValue={selectedWell.duct_outside_diameter}
                                   onChange = {(e)=> {
                                    listWells[key].duct_outside_diameter= e.target.value
                                  }} />
                            </Col></>}
                          <Button type='primary' onClick={sendData}>Envíar datos</Button>
                          </Row>
                        </>}
                      </Col>
                    </Row> 
                  </Card>
                </Col>

          </>)
}


const styles = {
  col_well: {
    backgroundImage: `url(${img_pozo})`,
    backgroundPosition: 'center',
    backgroundSize: '180% auto',
    height: '400px',
    backgroundRepeat: 'no-repeat',
    width: '100%',
    marginTop: window.innerWidth > 800 ? '0px': '20px'
  },
  input: {
    position: 'absolute',
    width: '25%',
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
    padding:'0px',
  },
  col_datas_b: {
    paddingleft: '10px',
    paddingright: '10px',
    marginbottom: '100px',
  },
  col_tech: {
    padding: '3px'
  }, 
  tag: {
    margin: '3px'
  },
  colform:{
    paddingLeft:'10px',
    paddingTop: '10px'
  },
  col_wells: {
    paddingLeft: '10px',
    paddingTop: '10px'
  }
}


export default Wells
