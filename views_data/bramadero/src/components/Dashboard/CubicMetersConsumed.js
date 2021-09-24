/* eslint-disable array-callback-return */
import React, { useEffect, useState } from 'react'



import { Line } from "react-chartjs-2";
import api_novus from '../../api_novus/endpoints'

import {
  Button,
  ButtonGroup,
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
} from "variables/charts.js"

const CubicMetersConsumed = () => {

    
    const [labels, setLabels] = useState([])
    const [data, setData] = useState([])
    

    const getData = async()=> {
        try {

            var today = new Date()
            var today_ex = new Date()
            today_ex.setDate(today_ex.getDate()-7)

            
            var str_start_date = `${today_ex.getFullYear()}-${today_ex.getMonth()+1}-${today_ex.getDate()}`
            var str_finish_date = `${today.getFullYear()}-${today.getMonth()+1}-${today.getDate()}`            

            const request = await api_novus.data('3grecdi1va', str_start_date, str_finish_date, 1500)            
            var results = request.result
            var unique_labels = []

            console.log(request)
            results.map((x) => {              
                unique_labels.push(x.time.slice(0,10))     
                setData(data => [...data, x.value])
            })
            setLabels(()=>[...new Set(unique_labels)]) 
            
            return request.result          
        } catch(err) {
            console.log(err)
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
            <CardTitle tag="h2">Metros cúbicos consumidos(m3)</CardTitle>
          </Col>          
        </Row>
      </CardHeader>
      <CardBody>
        <div className="chart-area">                      
          <Line
            data={{      
              labels: labels,
              datasets: [
                {
                  label: "M3",
                  fill: true,          
                  borderColor: "#1f8ef1",
                  borderWidth: 2,
                  borderDash: [],
                  borderDashOffset: 0.0,
                  pointBackgroundColor: "#1f8ef1",
                  pointBorderColor: "rgba(255,255,255,0)",
                  pointHoverBackgroundColor: "#1f8ef1",
                  pointBorderWidth: 20,
                  pointHoverRadius: 4,
                  pointHoverBorderWidth: 15,
                  pointRadius: 6,
                  data: data,
                },
              ],
            }}
            options={chart_1_2_3_options}
          />
        </div>
      </CardBody>
    </Card>
  </Col>)
}


export default CubicMetersConsumed