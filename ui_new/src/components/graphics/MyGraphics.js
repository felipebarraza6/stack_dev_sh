import React, { useState, useEffect, useContext } from 'react'
import { Typography, Row, Col, Button, Skeleton } from 'antd'
import { Area, Line } from '@ant-design/plots'
import { AppContext } from '../../App'
import api_novus from '../../api/novus/endpoints'
import { getNovusData1 } from './controller'

const { Title } = Typography

const MyGraphics = () => {

    const [option, setOption] = useState(0)
    const [load, setLoad] = useState(false)
    const [data1, setData1] = useState([])
    const [data2, setData2] = useState([])
    const [data3, setData3] = useState([])

    const {state, dispatch} = useContext(AppContext)

    const config1 = {
      data:  data1,        
      color: 'rgb(57,104,169, 0.4)',
      meta: {
        'm3/hora': {
          min: Math.min(...data1.map(o => o['m3/hora'])), 
          max: Math.max(...data1.map(o => o['m3/hora'])) + 5 
,
        },
      },
      xField: 'date',
      yField: 'm3/hora',  
      point: {
        size:3,
        style: {
          opacity: '0.2:',
          fill: 'white',
          stroke: '#3968A9',
          lineWidth: 2,
        },
      },
      yAxis: {
        title: {
          text: 'METROS CÚBICOS',
          style: {
            fontSize: 13,
          },
        },
      },
      xAxis: {
        title: {
          text: 'HORAS',
          style: {
            fontSize: 13,
          },
        },
      },
      label: {
        style: {
          fill: '#1F3461',
          fontSize: 15,
        }
      }
    }

    const config2 = {
      data:  data2,        
      color: 'rgb(57,104,169, 0.4)',
      meta: {
        'm3/dia': {
          min: Math.min(...data2.map(o => o['m3/dia'])), 
          max: Math.max(...data2.map(o => o['m3/dia'])) + 5 
,
        },
      },
      xField: 'date',
      yField: 'm3/dia',  
      point: {
        size:3,
        style: {
          opacity: '0.2:',
          fill: 'white',
          stroke: '#3968A9',
          lineWidth: 2,
        },
      },
      yAxis: {
        title: {
          text: 'METROS CÚBICOS',
          style: {
            fontSize: 13,
          },
        },
      },
      xAxis: {
        title: {
          text: 'DIAS DEL MES',
          style: {
            fontSize: 13,
          },
        },
      },
      label: {
        style: {
          fill: '#1F3461',
          fontSize: 15,
        }
      }
    }

    const config3 = {
      data:  data3,        
      color: 'rgb(57,104,169, 0.4)',
      meta: {
        'm/dia': {
          min: Math.min(...data3.map(o => o['m/dia'])), 
          max: Math.max(...data3.map(o => o['m/dia'])) + 5 
,
        },
      },
      xField: 'date',
      yField: 'm/dia',  
      point: {
        size:3,
        style: {
          opacity: '0.2:',
          fill: 'white',
          stroke: '#3968A9',
          lineWidth: 2,
        },
      },
      yAxis: {
        title: {
          text: 'METROS',
          style: {
            fontSize: 13,
          },
        },
      },
      xAxis: {
        title: {
          text: 'DIAS DEL MES',
          style: {
            fontSize: 13,
          },
        },
      },
      label: {
        style: {
          fill: '#1F3461',
          fontSize: 15,
        }
      }
    }

    const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    useEffect(()=> {
        getNovusData1(
          state, 
          api_novus, 
          setData1, 
          setData2, 
          setData3,
          setLoad, 
        option, dispatch)
      }, [option, state.selected_profile])


    return(<Row justify={'end'} align='middle' style={{paddingTop:'20px'}}>
        <Col span={6} style={{paddingLeft:'20px'}}>
            <Title level={2}>Gráficos</Title>
        </Col>
        <Col span={18} style={{float:'right'}}>
            <Button onClick={()=>setOption(0)} style={{margin:'5px', backgroundColor: option == 0 ?'white':'#1F3461', borderRadius:'10px', 
                            color:option == 0 ?'#1F3461':'white', borderColor:'#1F3461'}}>
                Acumulado(m³) - 24 horas
            </Button>
            <Button onClick={()=>setOption(1)} style={{margin:'5px', backgroundColor: option == 1 ?'white':'#1F3461', borderRadius:'10px', 
                            color:option == 1 ?'#1F3461':'white', borderColor:'#1F3461'}}>
                Acumulado(m³) - mensual
            </Button>
            <Button onClick={()=>setOption(2)} style={{margin:'5px', backgroundColor: option == 2 ?'white':'#1F3461', borderRadius:'10px', 
                            color:option == 2 ?'#1F3461':'white', borderColor:'#1F3461'}}>
                Nivel freático(m) - mensual
            </Button>
        </Col>
        <Col span={24} style={{paddingTop:'40px'}}>
            {load ? <>
                <Skeleton active round={true} style={{paddingLeft:'20px', paddingRight:'20px'}} />
                <Skeleton active round={true} style={{paddingLeft:'20px', paddingRight:'20px'}} />
                <Skeleton active round={true} style={{paddingLeft:'20px', paddingRight:'20px'}} />
            </>:<>
                {option==0 && <>
                  <Typography.Paragraph style={{marginLeft:'20px'}}>
                    Volumen acumulado del día <b>{new Date().getDate() -1} de {monthNames[new Date().getMonth()]} </b> en metros cúbicos.
                  </Typography.Paragraph>
                  <Line {...config1} />
                </>}
                {option==1 && <>
                  <Typography.Paragraph style={{marginLeft:'20px'}}>
                    Volumen acumulado desde el <b>01 al {new Date().getDate()-1} de {monthNames[new Date().getMonth()]}</b> en metro cúbicos.
                  </Typography.Paragraph>
                  <Line {...config2} />
                </>}
                {option==2 && <>
                  <Typography.Paragraph style={{marginLeft:'20px'}}>
                    Promedio nivel freático desde el <b>01 al {new Date().getDate()-1} de {monthNames[new Date().getMonth()]}</b> en metros.
                  </Typography.Paragraph>
                  <Area {...config3} />
                </>}
            </>}                                    
        </Col>
    </Row>)
}


export default MyGraphics
