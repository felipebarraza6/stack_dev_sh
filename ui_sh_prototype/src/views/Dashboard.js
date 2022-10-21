
import React, { useState, useEffect } from "react";
// nodejs library that concatenates classes

// reactstrap components
import {
  Card,  
  CardBody,
  CardTitle,
  Row,
  Col, Button, Input
} from "reactstrap";

import { Statistic, notification} from 'antd';
import api_novus from '../api_novus/endpoints'
import api_crm from '../api_crm/endpoints' 

import CubicMetersConsumed from "../components/Dashboard/CubicMetersConsumed"

const { Countdown } = Statistic;
const deadline = Date.now() + 0 * 60 * 60 * 24 * 2 + 1000 * 60; 

const Dashboard = () => {

  const [well, setWell] = useState(0)
  const [pond, setPond] = useState(0)
  const user = JSON.parse(localStorage.getItem('user') || null)
  const selected_sensor = JSON.parse(localStorage.getItem('selected_sensor') || null)
  const [billing, setBilling] = useState(0)
  const [listHistorial, setListHistorial] = useState([])
  const [listHistorialAdmin, setListHistorialAdmin] = useState([])
  const [selectProfileData, setSelectProfileData] = useState(selected_sensor.id)


  const today = new Date()
  

  useEffect(() => {
      const get = async() => {
          const rqHistory = await api_crm.billing_data(selectProfileData).then((r)=>setListHistorial(r.results))
          const rqHistoryAdmin = await api_crm.billing_data_admin().then((r)=>setListHistorialAdmin(r.results))
          const rqWell = await api_novus.lastData('3grecuc1v')
          const rqPond = await api_novus.lastData('3grecuc2v')
          if(rqPond.data.result.length > 0){
            if(rqPond.data.result[0].value === 3276.7){
              setPond(50) 
            }else {
              setPond(rqPond.data.result[0].value)
            }
          }
          setWell(rqWell.data.result[0].value)
          return {
            rqWell, 
            rqPond
          }
      }
    get()
  }, [])


  
  return (
    <>
      <div className="content">
    {<Row style={{marginBottom:'20px'}}>
              <>
            {user.profile_data.map((x)=> {
              return(<Col xs={2} key={x.id}>
                <Button onClick={()=> {
                  setSelectProfileData(x.id)
                  localStorage.setItem("selected_sensor", JSON.stringify({...x}))
                  localStorage.setItem("token_novus", x.token_service)
                  localStorage.setItem("data_p", JSON.stringify({
                    "d1": x.d1,
                    "d2": x.d2,
                    "d3": x.d3,
                    "d4": x.d4,
                    "d5": x.d5,
                    "d6": x.d6
                  }))
                  window.location.reload()

                }}>{x.title}</Button></Col>)
                })}
              </>
        </Row>}
        <Row>
              
          <CubicMetersConsumed />          
          <Col lg="4" md="6">
            <Card className="card-stats">
              <CardBody>
                <Row>
                  <Col xs="5">
                    <div className="info-icon text-center icon-warning">
                      <i className="tim-icons icon-components" />
                    </div>
                  </Col>
                  <Col xs="7">
                    <div className="numbers">
                      <p className="card-category">Caudal (lt/s)</p>
                      {user.username==='gcastro' ?<> 

                        <CardTitle tag="h3">{pond}</CardTitle>
                        EN DESARROLLO...
                        </>:<>
                          {user.username==='pozos_iansa' ? 
                            <CardTitle tag="h3">{pond}</CardTitle>:
                            <CardTitle tag="h3"> {well} </CardTitle>
                          }
                        </>
                      }
                    </div>
                  </Col>
                </Row>
              </CardBody>              
            </Card>
          </Col>
          <Col lg="4" md="6">
            <Card className="card-stats">
              <CardBody>
                <Row>
                  <Col xs="5">
                    <div className="info-icon text-center icon-primary">
                      <i className="tim-icons icon-components" />
                    </div>
                  </Col>
                  <Col xs="7">
                    <div className="numbers">
                      <p className="card-category">Nivel freático (mcH2O)</p>
                      {user.username==='gcastro'  ? 
                      <CardTitle tag="h3"> {well} </CardTitle>:
                        <>
                          {user.username=='pozos_iansa'  ? 
                            <CardTitle tag="h3"> {well} </CardTitle>: 
                            <CardTitle tag="h3"> {pond} </CardTitle>
                          }
                        </>
                      }
                    </div>
                  </Col>
                </Row>
              </CardBody>              
            </Card>
          </Col>
          <Col lg="4" md="6">
            <Card className="card-stats">
              <CardBody>
                <Row>
                  <Col xs="5">
                    <div className="info-icon text-center icon-success">
                      <i className="tim-icons icon-components" />
                    </div>
                  </Col>
                  <Col xs="7">
                    <div className="numbers">
                      <p className="card-category">Tiempo para sincronización</p>
                      <Countdown valueStyle={{color: 'gray'}} value={deadline} format="mm:ss:SSS" onFinish={()=> {
                        window.location.reload()
                      }
                      } />
                    </div>
                  </Col>
                </Row>
              </CardBody>              
            </Card>
          </Col>        
        </Row>
        <Row>          
          {user.profile_data[0].is_apr && <Card className="card-stats">
              <CardBody>
                <Row>    
                  <Col xs="12">
                    <div className="numbers">
                    <center>
                      <p className="card-category">
                        INGRESA EL TOTAL FACTURADO DEL <b>
                          {today.getMonth() < 10 ? <>0{today.getMonth()}</>:<>{today.getMonth()}</>} - {today.getFullYear()}
                        </b> (metros cúbicos)</p>
                        <input 
                          onChange={(e)=>setBilling(e.target.value)}
                          style={{
                              borderColor:'#263148',
                              borderRadius:'8px',
                              padding:'10px',
                              width:'200px', 
                              marginTop:'10px', 
                              marginBottom:'10px'
                          }} 
                          placeholder='Rango: 0 - 20.000.000,00' />
                      <Button onClick={()=> {
                        notification.success({message:'DATO INGRESADOS CORRECTAMENTE, TUS DATOS SE PROCESARAN EN 24/horas',placement:'top'})
                      }} style={{padding:'10px', marginLeft:'10px'}}>ACEPTAR</Button>
                    </center>
                    </div>
                  </Col> 
                  <Col xs="12">
                    <div className="numbers">
                    <center>
                      <h4 style={{marginTop:'30px'}}>HISTORIAL</h4>
                      <table style={styles.table}>
                          <tr >
                            <th style={styles.table.tdth}>Fecha</th>
                            <th style={styles.table.tdth}>Producción (m3)</th>
                            <th style={styles.table.tdth}>Facturación (m3)</th>
                            <th style={styles.table.tdth}>Estanques llenados mes</th>
                            <th style={styles.table.tdth}>Estanques llenados día</th>
                            <th style={styles.table.tdth}>% de perdida mensual</th>
                            <th style={styles.table.tdth}>m3 perdida en red</th>
                          </tr>
                          {listHistorial.map((x)=> {

                            var val_pro = ((x.production-x.billing)/x.production)
                            var val_pro_str = `${val_pro}`
                              return(<tr>
                                <th style={styles.table.tdth}>{x.month}</th>
                                <th style={styles.table.tdth}>{x.production}</th>
                                <th style={styles.table.tdth}>{x.billing}</th>
                                <th style={styles.table.tdth}>{parseFloat(x.production/x.constant_a).toFixed(1)}</th>
                                <th style={styles.table.tdth}>{parseFloat((x.production/x.constant_a)/31).toFixed(1)}</th>
                                <th style={styles.table.tdth}>{val_pro_str.slice(2,4)}%</th>
                                <th style={styles.table.tdth}>{x.production-x.billing}</th>
                              </tr>)
                          })} 
                                                   
                        </table>
                    </center>
                    </div>
                  </Col>
                  {user.is_staff && 
                    <Col xs="12">
                    <div className="numbers">
                    <center>
                      <h4 style={{marginTop:'30px'}}>HISTORIAL ADMINISTRADOR</h4>
                      <table style={styles.table}>
                          <tr >
                            <th style={styles.table.tdth}>APR</th>
                            <th style={styles.table.tdth}>Fecha</th>
                            <th style={styles.table.tdth}>Producción (m3)</th>
                            <th style={styles.table.tdth}>Facturación (m3)</th>
                            <th style={styles.table.tdth}>Estanques llenados mes</th>
                            <th style={styles.table.tdth}>Estanques llenados día</th>
                            <th style={styles.table.tdth}>% de perdida mensual</th>
                            <th style={styles.table.tdth}>m3 perdida en red</th>
                          </tr>
                          {listHistorialAdmin.map((x)=> {

                            var val_pro = ((x.production-x.billing)/x.production)
                            var val_pro_str = `${val_pro}`
                              return(<tr>
                                <th style={styles.table.tdth}>{x.profile.title}</th>
                                <th style={styles.table.tdth}>{x.month}</th>
                                <th style={styles.table.tdth}>{x.production}</th>
                                <th style={styles.table.tdth}>{x.billing}</th>
                                <th style={styles.table.tdth}>{parseFloat(x.production/x.constant_a).toFixed(1)}</th>
                                <th style={styles.table.tdth}>{parseFloat((x.production/x.constant_a)/31).toFixed(1)}</th>
                                <th style={styles.table.tdth}>{val_pro_str.slice(2,4)}%</th>
                                <th style={styles.table.tdth}>{x.production-x.billing}</th>
                              </tr>)
                          })} 
                                                   
                        </table>
                    </center>
                    </div>
                  </Col>

                  }
                </Row>
              </CardBody>              
            </Card>}
        </Row>
        
      </div>
    </>
  );
};


const styles = {
  table: {
    borderCollapse: 'collapse',
    width: '100%',    
    tdth: {
      border: '1px solid #dddddd',
      textAlign: 'left',
      padding: '8px'
    }
        
   }

}

export default Dashboard;
