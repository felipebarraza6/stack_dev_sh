
import React from "react";
import { Card, CardHeader, CardTitle, Row, Col } from "reactstrap";


const Charts2 = () => {
  return (
    <>
      <div className="content">
        <h2 className="text-center" style={{color: 'white'}} >Analisis de datos</h2>      
        <div style={{marginBottom:'0px'}}>

        </div>
        <Row className="mt-5">
          <Col className="ml-auto" md="4">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">Dia maximo de consumo del mes</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-chart-bar-32 text-primary" />{" "}
                  6332 / 3-JUN
                </CardTitle>
              </CardHeader>
            </Card>
          </Col>

          <Col className="ml-auto" md="4">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">Cantidad de estanques llenados las ultimas 24 hrs</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-chart-bar-32 text-primary" />{" "}
                  2
                </CardTitle>
              </CardHeader>
            </Card>
          </Col>

          <Col className="ml-auto" md="4">
            <Card className="card-chart">
              <CardHeader>                
                <h5 className="card-category">Recuperacion de pozo</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-chart-bar-32 text-info" /> 0 Seg (en desarrollo)
                </CardTitle>
              </CardHeader>              
            </Card>
          </Col>
        </Row>        
      </div>
    </>
  );
};

export default Charts2;
