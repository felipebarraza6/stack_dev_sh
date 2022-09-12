import React, { useEffect, useState } from "react";

import { Card, CardBody, CardTitle, Button, CardHeader } from "reactstrap";

import { Bar, Line } from "react-chartjs-2";
import { Input, Badge, Col, Row } from "antd";

import SortingTable from "../components/SortingTable/SortingTable.js";
import Pozo from "../assets/pozo/dem1.png";
import Img_acc from "../assets/pozo/acc.png"
import {
  chartExample5,
  chartExample6,
  chartExample7,
  chartExample8,
  chartExample9,
  chartExample10,
} from "../variables/charts.js";

import api_novus from "../api_novus/endpoints";
import imgwatter from "../assets/pozo/pozo y tanque-21.png";
import bomb from "../assets/pozo/pozo y tanque-19.png";

const MiPozo = () => {
  const [well, setWell] = useState(0);
  const [pond, setPond] = useState(0);
  const [acc, setAcc] = useState(0);

  const data_estatic = JSON.parse(localStorage.getItem("data_p"));

  const selected_sensor = JSON.parse(
    localStorage.getItem("selected_sensor") || null
  )

  const get = async () => {
    const rqWell = await api_novus.lastData("3grecuc1v");
    const rqPond = await api_novus.lastData("3grecuc2v");
    const rqAcc = await api_novus.lastData("3grecdi1va");
    setWell(rqWell.data.result[0].value);
    setPond(rqPond.data.result[0].value);
    setAcc(rqAcc.data.result[0].value);
    return {
      rqWell,
      rqPond,
      rqAcc,
    };
  };

  useEffect(() => {
    get();
  }, []);

  let watter2 = {
    marginTop: `${-40 - pond}px`,
    marginLeft: "-16px",
    position: "absolute",
  };

  return (
    <>
      <div className="content">
        <Row>
          <Col span={24}>
            <Card className="card-chart">
              <CardHeader style={{ marginBottom: "90px" }}>
                <Row>
                  <Col>
                    <h5 className="card-category">Mi Pozo</h5>
                    <CardTitle tag="h2">Esquema de representacion</CardTitle>

                    <Button
                      size="sm"
                      style={{ zIndex: "3" }}
                      onClick={() => {
                        get();
                      }}
                    >
                      ACTUALIZAR DATOS
                    </Button>
                  </Col>
    <Col style={{marginLeft:'400px'}}>

                    <table style={styles.table}>
                      <tr>
                        <th style={styles.table.tdth}>Profundidad de pozo</th>
                        <td style={styles.table.tdth}>
                          {data_estatic.d1} mtrs
                        </td>
                      </tr>
                      <tr>
                        <th style={styles.table.tdth}>
                          Posicionamiento de bomba
                        </th>
                        <td style={styles.table.tdth}>
                          {data_estatic.d3} mtrs
                        </td>
                      </tr>
                      <tr>
                        <th style={styles.table.tdth}>
                          Posicionamiento de sensor(freatico)
                        </th>
                        <td style={styles.table.tdth}>
                          {data_estatic.d2} mtrs
                        </td>
                      </tr>
                      <tr>
                        <th style={styles.table.tdth}>
                          Diámetro ducto de salida(bomba)
                        </th>
                        <td style={styles.table.tdth}>{data_estatic.d4}”</td>
                      </tr>
                      <tr>
                        <th style={styles.table.tdth}>Diámetro flujometro</th>
                        <td style={styles.table.tdth}>{data_estatic.d5}”</td>
                      </tr>
                    </table>
                  </Col>
                </Row>
              </CardHeader>
              <CardBody>
               
                <Row>
                  
                  <Col span={6}></Col>
                    <Col
                    span={12}
                    style={{
                      marginLeft:'-210px',
                      marginTop: "-199px",
                      backgroundImage: `url(${Pozo})`,
                      backgroundPosition: "absolute",
                      backgroundSize: "100% auto",
                      height: "500px",
                      backgroundRepeat: "no-repeat",
                      width: "100%",
                    }}
                  >
                    <div>
                      <div>
                        <Badge
                          status="processing"
                          text={
                            <>
                            {acc} <b>M3</b>
                            </>
                          }
                          style={styles.badge_acc}
                        />
                        <Badge
                          status="processing"
                          text={
                            <>
                             {pond} <b>Mtrs</b>
                            </>
                          }
                          style={styles.badge_level}
                        />
                        <Badge
                          status="processing"
                          text={
                            <>
                            {well} <b>Ltrs</b>
                            </>
                          }
                          style={styles.badge_well}
                        />
                        <img src={bomb} style={styles.bomb} />
                        <img src={imgwatter} style={styles.watter} />
                        <img src={imgwatter} style={watter2} />
                      </div>
                    </div>
                  </Col>

                                  </Row>
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row></Row>
      </div>
    </>
  );
};

const styles = {
  badge_well: {
    position: "absolute",
    marginLeft: "170px",
    zIndex: "3",
    marginTop: "160px",
    backgroundColor: "white",
    padding: "5px",
    border: "2px solid #1890ff",
    borderRadius: "5px",
  },


badge_acc2: {
    position: "absolute",
    marginLeft: "100px",
    zIndex: "3",
    marginTop: "70px",
    backgroundColor: "white",
    padding: "5px",
    border: "2px solid #1890ff",
    borderRadius: "5px",
  },
  badge_acc: {
    position: "absolute",
    marginLeft: "340px",
    zIndex: "3",
    marginTop: "170px",
    backgroundColor: "white",
    padding: "5px",
    border: "2px solid #1890ff",
    borderRadius: "5px",
  },
  badge_level: {
    position: "absolute",
    marginLeft: "330px",
    zIndex: "3",
    marginTop: "370px",
    backgroundColor: "white",
    padding: "5px",
    border: "2px solid #1890ff",
    borderRadius: "5px",
  },

  bomb: {
    marginTop: "20px",
    marginLeft: "25px",
    position: "absolute",
    zIndex: "2",
  },
  watter: {
    marginTop: "-5px",
    marginLeft: "-16px",
    position: "absolute",
  },
  line: {
    color: "white",
    backgroundColor: "#5e72e4",
    border: "10px solid #5e72e4",
    marginTop: "20px",
    marginLeft: "-16px",
    width: "200px",
  },
  line2: {
    color: "white",
    backgroundColor: "#5e72e4",
    border: "10px solid #5e72e4",
    marginTop: "-5px",
    marginLeft: "-50px",
    width: "80px",
  },
  diagonal: {
    borderTop: "4px solid gray",
    width: "57px",
    transform: "rotate(-12.5deg)",
    transformOrigin: "0% 0%",
    marginTop: "50px",
  },
  hrV: {
    height: "50vh",
    marginTop: "-5px",
    width: ".2vw",
    border: "10px solid #5e72e4",
    backgroundColor: "#5e72e4",
  },
  table: {
    borderCollapse: "collapse",
    width: "100%",
    tdth: {
      border: "1px solid #dddddd",
      textAlign: "left",
      padding: "8px",
    },
  },
};

export default MiPozo
