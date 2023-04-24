import React, { useContext, useEffect, useState } from 'react'
import { Row, Col, Typography,
        Input, Card } from 'antd'

import caudal_img  from '../../assets/images/caudal.png'
import nivel_img  from '../../assets/images/nivel.png'
import acumulado_img  from '../../assets/images/acumulado.png'
import pozo1  from '../../assets/images/pozo1.png'
import { AppContext } from '../../App'
import api_novus from '../../api/novus/endpoints'
import { getNovusData } from './controller'

const { Title } = Typography

const numberForMiles = new Intl.NumberFormat('de-DE')

const MyWell = () => {

    const { state } = useContext(AppContext)
    const [caudal, setCaudal] = useState(0.0)
    const [nivel, setNivel] = useState(0.0)
    const [acumulado, setAcumulado] = useState(0)

    

    useEffect(()=> {
        getNovusData(setCaudal, setNivel, state, api_novus, setAcumulado, acumulado, nivel)

    }, [state.selected_profile])

    return(<Row justify={'center'} style={{padding:'20px'}}>
                <Col span={24}>
                    <Title level={2}>Mi Pozo</Title>
                </Col>       
                <Col span={window.innerWidth > 900 ? 6:24}>                                    
                    <Card hoverable style={{marginBottom:'10px', marginTop:'20px', border:'solid 1px grey', borderRadius:'15px', width:'350px'}}>
                        <Row align='middle'>
                            <Col span={7}><img src={caudal_img} width='60px'  /></Col>
                            <Col span={12}><Title level={5} style={{color:'#222221'}}>Caudal</Title></Col>
                            <Col span={12} offset={7} style={{marginTop:'-15px'}}>
                              <Typography.Paragraph level={5}>
                                {parseFloat(caudal).toFixed(1)==='3276.7' ? 
                                <div style={{color:'red'}}>{parseFloat(caudal).toFixed(1)}</div>
                                  :
                                <b>{parseFloat(caudal).toFixed(1)} (Litros/seg)</b>
                                }
                              </Typography.Paragraph>
                            </Col>
                        </Row>                                    
                    </Card>
                    
                    <Card hoverable style={{marginBottom:'10px', marginTop:'20px', border:'solid 1px grey', borderRadius:'15px', width:'350px'}}>
                               <Row align='middle'>
                                   <Col span={7}><img src={nivel_img} width='60px' /></Col>
                                   <Col span={12}><Title level={5} style={{color:'#222221'}}>Nivel Freático</Title></Col>                                            
                                   <Col span={12} offset={7} style={{marginTop:'-25px'}}><Typography.Paragraph level={5}><b>{parseFloat(nivel).toFixed(1)} (Metros)</b></Typography.Paragraph></Col>
                               </Row>                                    
                           </Card>
                           <Card hoverable style={{marginBottom:'50px', marginTop:'20px', border:'solid 1px grey', borderRadius:'15px', width:'350px'}}>
                               <Row align='middle'>
                                    <Col span={7}><img src={acumulado_img} width='60px'  /></Col>
                                    <Col span={17}><Title level={5} style={{color:'#222221'}}>Acumulado</Title></Col>                                            
                                    <Col span={12} offset={7} style={{marginTop:'-22px'}}>
                                    <Typography.Paragraph level={5}><b>{state.user.username === 'fermin'  ? numberForMiles.format(acumulado*1) :state.selected_profile.title=='PAINE' ? '6094':numberForMiles.format(acumulado)}</b><br/></Typography.Paragraph>
                                    <Typography.Paragraph level={5} style={{marginTop:'-20px'}}><b>(Metros cúbicos)</b></Typography.Paragraph>
                                    </Col>
                                    
                               </Row>                                    
                           </Card>
                       </Col>
                       {window.innerWidth > 900 &&
                       <Col span={18} style={{paddingLeft:'140px', paddingTop:'70px'}}>
                           <center>
                               <img src={pozo1} width={'430px'} style={{position:'absolute', marginLeft:'-240px', marginTop:'-80px'}} />                                        
                           </center>
                               <Input disabled style={{color:'white',backgroundColor: parseFloat(caudal).toFixed(1) ==='3276.7'?'#cf1322':'#1F3461',border:'0px solid #1F3461', fontSize:'17px',width: parseFloat(caudal).toFixed(1) === '3276.7'? '80px':'150px', marginTop:'30px', marginLeft:'100px', position:'absolute', borderRadius:'10px'}} 
                               value={parseFloat(caudal).toFixed(1) ==='3276.7' ? `${parseFloat(caudal).toFixed(1)}`:`${parseFloat(caudal).toFixed(1)} (Litros/seg)`} />

                               <Input disabled style={{color:'white',backgroundColor:'#1F3461',border:'0px solid #1F3461', fontSize:'17px',width:'160px', marginTop:'5px', marginLeft:'320px', position:'absolute', borderRadius:'10px'}} value={`${state.user.username === 'fermin'  ? numberForMiles.format(acumulado*1) :state.selected_profile.title=='PAINE' ? '6094':numberForMiles.format(acumulado)} (m³)`} />
                               <Input disabled style={{color:'white',backgroundColor:'#1F3461',border:'0px solid #1F3461', fontSize:'17px',width:'110px', marginTop:'260px', marginLeft:'300px', position:'absolute', borderRadius:'10px'}} value={`${parseFloat(nivel).toFixed(1)} (m)`}  />                               
                       </Col>}
                       <Col>
                       </Col>
                   </Row>)
}

export default MyWell
