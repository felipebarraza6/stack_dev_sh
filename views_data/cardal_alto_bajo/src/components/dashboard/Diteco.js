import React, { useState, useEffect } from 'react'
import { Line } from 'react-chartjs-2'
import {getting_list_diteco} from '../../novus_toga/endpoints'
import { Skeleton, Row, Col, Table, Typography } from 'antd'
const { Title } = Typography 


const Diteco = () => {
    const [loading, setLoading] = useState(false)
    var optionsLines = {
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: false,
              },
            },
          ],
        },
      }

      var date_7_days = new Date() 
    date_7_days.setDate(date_7_days.getDate() -30)  
    let day = date_7_days.getDate()
    let month = date_7_days.getMonth() + 1
    let year= date_7_days.getFullYear()
    let string_date = `${year}-${month}-${day}`
    if(month < 10){
      string_date = `${year}-0${month}-${day}`
    }  
    
    var date_today = new Date()
    let day_t = date_today.getDate()
    let month_t = date_today.getMonth() + 1
    let year_t = date_today.getFullYear()
    let string_date_today = `${year_t}-${month_t}-${day_t}`
    if(month_t < 10){
      string_date_today = `${year_t}-0${month_t}-${day_t}`
    }

    const initialFreatic = {
        'values': null,
        'start_date': string_date,
        'end_date': string_date_today,
        'last_values': null,
        'dataCharts':null
      }  
      
      const initialFlow = {
        'values': null,
        'start_date': string_date,
        'end_date': string_date_today,
        'last_values': null,
        'dataCharts': null
        }
  
      const [freatic, setFreatic] = useState(initialFreatic)
      const [flow, setFlow] = useState(initialFlow)  

      useEffect(()=> {
        setLoading(true)
        const get_freatic = async() => {
            var values = []
            var prom = 0
            var last_values = []
  
            const request_all = await  getting_list_diteco(
                '3grecuc1v',
                freatic.start_date,
                freatic.end_date,
                '1000000'
            ).then((response)=> {
                if(response.status === 200){
                    const values_freatic = response.data.result
                    let calc = 0
                    values_freatic.map((element)=>{
                      calc+=element.value
                    })
                    calc = calc / values_freatic.length
                    values = response.data.result
                    prom = calc

                    setLoading(false)
                }
            })
            var dates_labels= []
            var dates_string=[]
            var data_values=[]
            var data_numbers=[]
            values.map((element, index)=>{
              values[index] = {
                ...values[index],
                'date_format':`${element.time.slice(5,10)}`,
                'date_table': `${element.time.slice(0,10)} - ${element.time.slice(11,19)} hrs.`,
                'MTRS': element.value
              }
              if(!dates_labels.includes(values[index].date_format)){
                dates_labels[index] = values[index].date_format
                dates_string.push(values[index].date_format)
               }
              if(!data_values.includes(values[index].value)){
                data_values[index] = values[index].value
                data_numbers.push(values[index].value)
               }
              })
  
              setFreatic({
                  ...freatic,
                  values: values,
                  prom: prom,
                  last_values: last_values,
                  dataCharts: {
                   labels: dates_string,
                   datasets: [
                        {
                           label: 'Nivel Freático - MTRS',
                           data: data_numbers,
                           fill:false,
                           backgroundColor: 'rgb(1, 15, 119)',
                           borderColor: 'rgba(1, 15, 119, 0.2)',
                         }
                        ]
                        }
              })
              return {
                  request_all,
              }
          }
  
          const get_flow = async() => {
            var values = []
            var prom = 0
            var last_values = []
  
            const request_all = await getting_list_diteco(
                '3grecuc2v',
                flow.start_date,
                flow.end_date,
                '1000000'
            ).then((response)=>{
              if(response.status === 200){
                  const values_flow = response.data.result
                  let calc = 0
                  values_flow.map((element)=>calc+=element.value)
                  calc = calc / values_flow.length
                  values = response.data.result
                  prom = calc
              }
            })
            var dates_labels = []
            var dates_string = []
            var data_values = []
            var data_numbers = []
            values.map((element, index)=> {
              values[index] = {
                ...values[index],
                'date_format':`${element.time.slice(5,10)}`,
                'date_table': `${element.time.slice(0,10)} - ${element.time.slice(11,19)} hrs.`,
                'LTRS': element.value
              }
              if(!dates_labels.includes(values[index].date_format)){
                dates_labels[index] = values[index].date_format
                dates_string.push(values[index].date_format)
              }
              if(!data_values.includes(values[index].value)){
                data_values[index] = values[index].value
                data_numbers.push(values[index].value)
              }
            })
            
            setFlow({
                ...flow,
                values: values,
                prom: prom,
                last_values: last_values,
                dataCharts: {
                    labels: dates_string,
                    datasets: [
                      {
                        label: 'Flujo - LTRS',
                        data: data_numbers,
                        fill:false,
                        backgroundColor: 'rgb(1, 15, 119)',
                        borderColor: 'rgba(1, 15, 119, 0.2)',
                      }
                    ]
                }
  
            })
            return {
                request_all
            }
          }
          get_flow()
          get_freatic()
      
      },[])

      var columsFlow = []
    if(flow.dataCharts){
    columsFlow = [
      {
        title:'Variable',
        dataIndex: 'variable',
        key: 'variable'
      },
      {
        title:'Mes',
        dataIndex:'date_table',
        key:'date_format',

      },
      {
        title:'Valor',
        dataIndex:'value',
        key:'value'
      }

    ]
      }

    return(
      <>
        {loading ? <Skeleton />:
        <Row style={{marginTop:'40px'}}> 
                  <Col span={8} style={{marginRight:'20px'}}>
                  <Table size='middle' dataSource={freatic.values} columns={columsFlow}  />
                  </Col>
                    <Col span={15} style={{marginRight:'20px'}}>
                        <Title level={4} style={{textAlign:'center'}}>Nivel Freático / Metros</Title>
                        {freatic.values &&
                          <Line data={freatic.dataCharts} options={optionsLines} />
                        }
                   </Col>
                    <Col span={15} style={{marginLeft:'20px', marginTop:'100px'}} >
                        <Title level={4} style={{textAlign:'center'}}>Flujo / Litros</Title>
                        {flow.values &&
    
                            <Line data= {flow.dataCharts}  options = {optionsLines} />
                        }
                    </Col>
                    <Col span={8} style={{marginRight: '20px', marginTop:'100px'}}>
                      <Table
                          size='middle'
                          dataSource = {flow.values} 
                          columns={columsFlow} />
                    </Col>
                </Row>
        }
      </>
    )

}


export default Diteco
