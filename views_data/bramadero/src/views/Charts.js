/*!

=========================================================
* Black Dashboard PRO React - v1.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/black-dashboard-pro-react
* Copyright 2020 Creative Tim (https://www.creative-tim.com)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";
// react plugin used to create charts
import { Line } from "react-chartjs-2";
// reactstrap components
import { Card, CardHeader, CardBody, CardTitle, Row, Col } from "reactstrap";

// core components
import {
  chartExample5,
  chartExample6,  
} from "variables/charts.js";

const Charts = () => {
  return (
    <>
      <div className="content">
        <h2 className="text-center" style={{color: "white"}} >Nivel de pozo & Nivel de caudal</h2>      
        <div style={{marginBottom:'0px'}}>

        </div>
        <Row className="mt-5">
          <Col className="ml-auto" md="5">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">PROMEDIO EN METROS</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-chart-bar-32 text-primary" />{" "}
                  Nivel de pozo
                </CardTitle>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Line
                    data={chartExample5.data}
                    options={chartExample5.options}
                  />
                </div>
              </CardBody>
            </Card>
          </Col>
          <Col className="mr-auto" md="5">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">PROMEDIO EN LITROS</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-chart-bar-32 text-info" /> Nivel de caudal
                </CardTitle>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Line
                    data={chartExample6.data}
                    options={chartExample6.options}
                  />
                </div>
              </CardBody>
            </Card>
          </Col>
        </Row>        
      </div>
    </>
  );
};

export default Charts;
