import React, { useEffect, useState } from 'react'

// react plugin used to create charts
import { Line } from "react-chartjs-2";
import api_novus from '../../api_novus/endpoints'
// reactstrap components
import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  Row,
  Col
} from "reactstrap";

// core components
import {
  dashboard, chart_1_2_3_options
} from "../../variables/charts.js"

const CubicMetersConsumed = () => {

    const [labels, setLabels] = useState([])
    const [data, setData] = useState([])
    const user = JSON.parse(localStorage.getItem('user'))
    const selected_sensor = JSON.parse(localStorage.getItem('selected_sensor') || null)
 
   
    const getData = async()=> {
      var data_l = []
      var data_d = []
        try {            
            for(var i=0; i < 7; i++){              
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
                setLabels(label =>{                
                  data_l.push(results[0].time.slice(0, 10))
              })                            
                // eslint-disable-next-line no-loop-func
                setData(data => {     
                  data_d.push(parseFloat(results[0].value/selected_sensor.scale ).toFixed(2))
                })               
              }                                            
            }                      
            setLabels(data_l)
            setData(data_d)
        } catch(err) {
            console.log({err})
        }        
    }

    useEffect(() => {
        getData()                
    }, [])
    
    
    return(<Col xs="12">
    <Card className="card-chart">
      <CardHeader>
        <Row>
          <Col className="text-left" sm="6">
            <h5 className="card-category">Medida en metros cubicos</h5>
            <CardTitle tag="h2">Volumen acumulado (m3)</CardTitle>
          </Col>
        </Row>
      </CardHeader>
      <CardBody>
        <div className="chart-area">  
        {labels && 
          <Line
            data={{      
              labels: labels,
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
                  data: data
                },
              ],
            }}
            options={chart_1_2_3_options}
          />}
        </div>
      </CardBody>
    </Card>
  </Col>)
}


export default CubicMetersConsumed
