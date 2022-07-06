import React, {useState, useEffect} from "react";
// react plugin used to create charts
import { Line, Bar } from "react-chartjs-2";
// reactstrap components
import { Card, CardHeader, CardBody, CardTitle, Row, Col } from "reactstrap";

import api_novus from '../api_novus/endpoints'

// core components
import {
  chartExample5,
  chartExample6,
  chart_1_2_3_options,
  chart_mode
} from "../variables/charts.js";

const Charts = () => {

  const [labels1, setLabels1] = useState([])
  const [data1, setData1] = useState([])
  const [objD1, setObjD1] = useState([])

  const [labels2, setLabels2] = useState([])
  const [data2, setData2] = useState([])

  const [labels3, setLabels3] = useState([])
  const [data3, setData3] = useState([])

  const user = JSON.parse(localStorage.getItem('user'))
  const selected_sensor = JSON.parse(localStorage.getItem('selected_sensor') || null)

  


  const getDataFl = async()=> {
    
    var start_datenowi = new Date()
      try {            
          let list_d = []
          let rest = []
          let proto = []
          let labels= []
          for(var i=0; i <= 24; i++){            
            var start_datenow = new Date()                       
            var demo_date = new Date ()
            start_datenow.setDate(start_datenow.getDate()-i)
            const rq1 = await api_novus.data('3grecdi1va', 
              `${start_datenow.getFullYear()}-${start_datenow.getMonth()+1}-${start_datenow.getDate()}`,
              `${start_datenow.getFullYear()}-${start_datenow.getMonth()+1}-${start_datenow.getDate()}`
            )            
            var results = rq1.result
           
            // eslint-disable-next-line no-loop-func            
            if(results.length > 0){
              // eslint-disable-next-line no-loop-func
              proto.push({
                  date:results[0].time.slice(0, 10),
                  value: parseFloat(results[0].value ).toFixed(0)
              })

              labels.push(`${i}:00`)

              // eslint-disable-next-line no-loop-func
              
              list_d.push(parseFloat(results[0].value).toFixed(0))                         
             
            }               
          }  
          for(var i =0; i < list_d.length; i++){
              var proc = list_d[i]-list_d[i+1]
              if(!isNaN(proc)){
                var number = parseFloat(proc/selected_sensor.scale).toFixed(1)
                if(i===0){

                rest.push(number.slice('0')) 
                }else {

                rest.push(number.slice(1,3)) 
                }
              }              
          }  
          rest[0]= '0'
          setData1(rest)
          labels.pop()
          setLabels1(labels)
          
      } catch(err) {
          console.log({err})
      }        
  }

const getDataNl = async()=> {
    
    var start_datenowi = new Date()
      try {            
          let list_d = []
          let rest = []
          let proto = []
          let labels= []
          for(var i=0; i < start_datenowi.getDate(); i++){            
            var start_datenow = new Date()                       
            var demo_date = new Date ()
            start_datenow.setDate(start_datenow.getDate()-i)
            const rq1 = await api_novus.data('3grecuc2v', 
              `${start_datenow.getFullYear()}-${start_datenow.getMonth()+1}-${start_datenow.getDate()}`,
              `${start_datenow.getFullYear()}-${start_datenow.getMonth()+1}-${start_datenow.getDate()}`
            )            
            var results = rq1.result
           
            // eslint-disable-next-line no-loop-func            
            if(results.length > 0){
              // eslint-disable-next-line no-loop-func
              proto.push({
                  date:results[0].time.slice(0, 10),
                  value: parseFloat(results[0].value)
              })


              labels.push(results[0].time.slice(0, 10))

              // eslint-disable-next-line no-loop-func
              //
              console.log(results)
              if(results[0].value == -3200){
                list_d.push(51.00)
              }else {
                list_d.push(parseFloat(results[0].value))                         
              } 
             
            }               
          }  
           
          list_d.reverse()
          labels.reverse()
          setData3(list_d)
          setLabels3(labels)
          
      } catch(err) {
          console.log({err})
      }        
  }

  const getDataPw = async()=> {
    var data_v = []
    var start_datenowi = new Date()
    try {            
          let list_d = []
          let rest = []
          let proto = []
          let labels= []
          let token_date = new Date()
          for(var i=0; i < token_date.getDate() +1 ; i++){            
            var start_datenow = new Date()                       
            var demo_date = new Date ()
            start_datenow.setDate(start_datenow.getDate()-i)
            const rq1 = await api_novus.data('3grecdi1va', 
              `${start_datenow.getFullYear()}-${start_datenow.getMonth()+1}-${start_datenow.getDate()}`,
              `${start_datenow.getFullYear()}-${start_datenow.getMonth()+1}-${start_datenow.getDate()}`
            )            
            var results = rq1.result
           
            // eslint-disable-next-line no-loop-func            
            if(results.length > 0){
              // eslint-disable-next-line no-loop-func
              proto.push({
                  date:results[0].time.slice(0, 10),
                  value: parseFloat(results[0].value ).toFixed(1)
              })

              labels.push(results[0].time.slice(0, 10))

              // eslint-disable-next-line no-loop-func
              
              list_d.push(parseFloat(results[0].value).toFixed(1))                         
             
            }               
          }  
          for(var i =0; i < list_d.length; i++){
              var proc = list_d[i]-list_d[i+1]
              if(!isNaN(proc)){
                rest.push(proc/selected_sensor.scale).toFixed(1) 
              }              
          }  
          rest.reverse()
          setData2(rest)
          labels.pop()
          labels.reverse()
          setLabels2(labels)
          
      } catch(err) {
          console.log({err})
      } 
      
             
  }

  var acc_date = new Date()
  var month = acc_date.toLocaleString('default', { month: 'long' })

  useEffect(() => {
    getDataFl()         
    getDataPw()
    getDataNl()
}, [])

  return (
    <>
      <div className="content">
       
     
      <Row style={{marginTop:'100px'}}>
      <Col className="text-left" sm="12">
      <Card className="card-chart">  
      <CardHeader>       
            <CardTitle tag="h2">Acumulado (m3) - Últimas 24 horas </CardTitle>
      </CardHeader>          
      <CardBody>
        <div className="chart-area">                             
          <Line
            data={{      
              labels: labels1,
              datasets: [
                {
                  label: "M3",
                  fill: false,          
                  borderColor: "#1f8ef1",
                  borderWidth: 2,
                  borderDash: [],
                  borderDashOffset: 0.0,
                  pointBackgroundColor: "#1f8ef1",
                  pointBorderColor: "rgba(255,255,255,0)",
                  pointHoverBackgroundColor: "#1f8ef1",
                  pointBorderWidth: 0,
                  pointHoverRadius: 4,
                  pointHoverBorderWidth: 15,
                  pointRadius: 6,
                  data: data1,
                },
              ],
            }}
            options={chart_mode}
          />
        </div>
      </CardBody>
      </Card> 
        </Col> 
        <Col className="text-left" sm="12" style={{marginTop:'-10px', paddingBottom:'2%'}}>
            <h3 style={{paddingLeft:'10px'}}>{month.toUpperCase()}</h3>
        <table style={styles.table}>          
          <tr>
          
          {labels1.map((x, index)=>{
              if(index<=12){
                return(
                  <td style={styles.table.tdtha} >
              {x}
              </td>

                )
              }
            })}</tr>
            <tr>
            {data1.map((x, index)=>{ 
              if(index<=12){
              return(    
              <td style={styles.table.tdth}>
              {x.slice(0,4)}
              </td>)
          }
            }
            )}</tr>

<tr>
          
          {labels1.map((x, index)=>{
              if(index>12){
                return(
                  <td style={styles.table.tdtha} >
              {x}
              </td>

                )
              }
            })}</tr>
            <tr>
            {data1.map((x, index)=>{ 
              if(index>12){
              return(    
              <td style={styles.table.tdth}>
              {x.slice(0,2)}
              </td>)
          }
            }
            )}</tr>

        
        </table>
        </Col>
      </Row>
      <Row>
       <Col className="text-left" sm="12">
      <Card className="card-chart">  
      <CardHeader>       
            <CardTitle tag="h2">Acumulado (m3) - Último mes</CardTitle>
      </CardHeader>          
      <CardBody>
        <div className="chart-area">                             
          <Line
            data={{      
              labels: labels2,
              datasets: [
                {
                  label: "M3",
                  fill: false,          
                  borderColor: "#1f8ef1",
                  borderWidth: 2,
                  borderDash: [],
                  borderDashOffset: 0.0,
                  pointBackgroundColor: "#1f8ef1",
                  pointBorderColor: "rgba(255,255,255,0)",
                  pointHoverBackgroundColor: "#1f8ef1",
                  pointBorderWidth: 0,
                  pointHoverRadius: 4,
                  pointHoverBorderWidth: 15,
                  pointRadius: 6,
                  data: data2,
                },
              ],
            }}
            options={chart_mode}
          />
        </div>
      </CardBody>
      </Card> 
        </Col>  
        <Col>
          <table style={styles.table}>          
            <h3 style={{paddingLeft:'10px'}}>{month.toUpperCase()}</h3>
          <tr>
          {labels2.map((x)=>
              <td style={styles.table.tdtha} >
              {x.slice(8,10)}
              </td>
              
            )}</tr>
            <tr>
            {data2.map((x)=>
              <td style={styles.table.tdth}>
              {x} (m3)
              </td>
            )}</tr>
    <hr />
          <tr>
        <td style={styles.table.tdtha} >
          TOTAL
              </td>

        <td style={styles.table.tdth}>
        <b>{data2.reduce((a,b)=>(parseFloat(a)+parseFloat(b)),0)}</b>
        </td>
        </tr>

        </table>

        </Col>
        

      </Row>
      <Row style={{marginTop:'100px'}}>
      <Col className="text-left" sm="12">
      <Card className="card-chart">  
      <CardHeader>       
            <CardTitle tag="h2">Columna de agua(metros) - Último mes</CardTitle>
      </CardHeader>          
      <CardBody>
        <div className="chart-area">                             
          <Line
            data={{      
              labels: labels3,
              datasets: [
                {
                  label: "METROS",
                  fill: false,          
                  borderColor: "#1f8ef1",
                  borderWidth: 1,
                  borderDash: [],
                  borderDashOffset: 0.0,
                  pointBackgroundColor: "#1f8ef1",
                  pointBorderColor: "rgba(255,255,255,0)",
                  pointHoverBackgroundColor: "#1f8ef1",
                  pointBorderWidth: 0,
                  pointHoverRadius: 4,
                  pointHoverBorderWidth: 1,
                  pointRadius: 6,
                  data: data3,
                },
              ],
            }}
            options={chart_mode}
          />
        </div>
      </CardBody>
      </Card> 
        </Col> 
        <Col className="text-left" sm="12" style={{paddingTop:'0%'}}>
            <h3 style={{paddingLeft:'10px'}}>{month.toUpperCase()}</h3>
        <table style={styles.table}>          
          <tr>
          {labels3.map((x)=>
              <td style={styles.table.tdtha} >
              {x.slice(8, 10)}
              </td>
            )}</tr>
            <tr>
            {data3.map((x)=>
              <td style={styles.table.tdth}>
              {x}
              </td>
            )}</tr>
        </table>
        </Col>
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
    },
    tdtha: {
      border: '1px solid #dddddd',
      textAlign: 'left',
      padding: '8px',
      backgroundColor: 'grey',
      color:'white'
    },
    tdthr: {
      border: '1px solid #dddddd',
      textAlign: 'left',
      padding: '8px',
      color: 'red'
    },
    tdthb: {
      border: '1px solid #dddddd',
      textAlign: 'left',
      padding: '8px',
      color: '#1890ff'
    }
        
   }
}

export default Charts;
