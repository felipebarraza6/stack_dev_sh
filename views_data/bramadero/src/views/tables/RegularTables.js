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

// reactstrap components
import { Card, CardHeader, CardBody, CardTitle, Row, Col } from "reactstrap";

// core components
import SortingTable from "components/SortingTable/SortingTable.js";

const RegularTables = () => {
  return (
    <>
      <div className="content">
      <h2 className="text-center" style={{color: 'white'}} >Reportes</h2>  
        <Row>
          <Col className="mb-5" md="12">
            <Card>
              <CardHeader>
                <CardTitle tag="h4">LISTADO DE PERSONAS</CardTitle>
              </CardHeader>
              <CardBody>
                <SortingTable
                  thead={[
                    { text: "Nombre" },
                    { text: "Cargo" },
                    { text: "Telefono" },
                  ]}
                  tbody={[
                    {
                      data: [
                        { text: "Damian Huanque" },
                        { text: "Operador" },
                        { text: "+56 9 9617 7817" },
                      ],
                     },
                                                          
                  ]}
                />
              </CardBody>
            </Card>
          </Col>          
        </Row>
      </div>
    </>
  );
};

export default RegularTables;
