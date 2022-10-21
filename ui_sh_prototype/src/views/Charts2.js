import React, { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, Row, Col, CardBody } from "reactstrap";
import api_novus from "../api_novus/endpoints";
import api_crm from "../api_crm/endpoints";
import icono1 from "../assets/img/icono-20.png";
import icono2 from "../assets/img/icono-27.png";
import icono3 from "../assets/img/Icono-30.png";
import icono6 from "../assets/img/Icono-22.png";

import icono4 from "../assets/img/Icono-28.png";
import icono5 from "../assets/img/Icono-23.png";
import icono7 from "../assets/img/icono-21.png";

const Charts2 = () => {
  const [labels, setLabels] = useState([]);
  const [data, setData] = useState([]);
  const [values, setValues] = useState([]);
  const [viewstr, setViewStr] = useState("");
  const [valueMax, setValueMax] = useState(null);
  const [statElement, setStatElement] = useState(null);
  const [accTotal, setAccTotal] = useState(0);

  const data_p = JSON.parse(localStorage.getItem("data_p"));
  const user = JSON.parse(localStorage.getItem("user"));

  const selected_sensor = JSON.parse(
    localStorage.getItem("selected_sensor") || null
  );

  const stat1 = user.profile_data.in1;
  const stat2 = user.profile_data.in2;
  const stat3 = user.profile_data.in3;
  const stat4 = user.profile_data.in4;
  const stat5 = user.profile_data.in5;
  const stat6 = user.profile_data.in6;

  console.log(accTotal);

  const getData = async () => {
    var data_v = [];
    var start_datenowi = new Date();
    var rquest2 = await api_crm
      .billing_data(selected_sensor.id)
      .then((r) => setStatElement(r.results[0]));
    try {
      let list_d = [];
      let rest = [];
      let arrVal = [];
      let max = 0.0;
      let maxObj = {};
      for (var i = 0; i < 7; i++) {
        var start_datenow = new Date();
        var demo_date = new Date();
        start_datenow.setDate(start_datenow.getDate() - i);
        const rq1 = await api_novus.data(
          "3grecdi1va",
          `${start_datenow.getFullYear()}-${
            start_datenow.getMonth() + 1
          }-${start_datenow.getDate()}`,
          `${start_datenow.getFullYear()}-${
            start_datenow.getMonth() + 1
          }-${start_datenow.getDate()}`
        );
        var results = rq1.result;

        // eslint-disable-next-line no-loop-func
        if (results.length > 0) {
          // eslint-disable-next-line no-loop-func
          list_d.push({
            date: results[0].time.slice(0, 10),
            value: parseFloat(results[0].value),
          });
          if (i == 1) {
            setAccTotal(parseFloat(results[0].value));
          }
        }
      }

      for (var i = 0; i < list_d.length; i++) {
        if (list_d[i + 1]) {
          rest = parseFloat(list_d[i].value - list_d[i + 1].value);
          list_d[i].value = rest;
        }
      }

      //console.log(rest)
      for (var i = 0; i < list_d.length - 1; i++) {
        arrVal.push(list_d[i]);
      }
      for (var i = 0; i < arrVal.length; i++) {
        if (arrVal[i].value > max) {
          max = arrVal[i].value;
          maxObj = arrVal[i];
        }
      }

      Math.max.apply(
        Math,
        arrVal.map(function (o) {
          maxObj = o;
          return o.value;
        })
      );

      setValueMax(maxObj);
      //setData1(rest)
    } catch (err) {
      console.log({ err });
    }
  };

  useEffect(() => {
    getData();
  }, []);

  console.log(user);
  return (
    <>
      <div className="content" style={{ marginTop: "0px" }}>
        <div style={{ marginBottom: "0px" }}></div>

        
        {user.username == "pozos_iansa" || "pozos_iansaquepue" ? (
          <>
            <Row className="mt-5">
              <Col className="ml-center" md="5">
                <Card
                  className="card-chart"
                  style={{
                    background:
                      "linear-gradient(180deg, rgba(255,255,255,1) 30%, rgba(228,237,247,1) 61%, rgba(216,229,244,1) 69%, rgba(210,225,242,1) 79%, rgba(197,216,238,1) 87%, rgba(150,183,224,1) 100%, rgba(0,80,179,1) 100%)",
                  }}
                >
                  <CardHeader
                    style={{ border: "1px #3967AA solid", borderRadius: "7px" }}
                  >
                    <CardBody style={{ margin: "10px" }}>
                      <Row>
                        <Col>
                          <img
                            alt="icono"
                            src={icono6}
                            style={{ width: "40%" }}
                          />
                        </Col>
                        <Col>
                          <h4>Peak consumo, semana anterior</h4>
                        </Col>
                      </Row>
                      <Row>
                        <Col></Col>
                            <Col>
                              <div>
                                <h4>
                                  {selected_sensor.token_service == "867f9225-24f2-487d-bf28-c2ccd0e662bc" && 
                                    '369.97 (m3)'	
                                  }
                                  {selected_sensor.token_service == "32ae0a00-7374-46e8-bc5c-e085714748d7" && 
                                    '131.32 (m3)'	
                                  }

                                </h4>
                              </div>
                            </Col>
                            <Col>
                              <h4>
                                {selected_sensor.token_service == "867f9225-24f2-487d-bf28-c2ccd0e662bc" && 
                                    '2022-10-15'	
                                }
{selected_sensor.token_service == "32ae0a00-7374-46e8-bc5c-e085714748d7" && 
                                    '2022-10-10'	
                                  }


                              </h4>
                            </Col>
                      </Row>
                    </CardBody>
                    <Row>
                      <Col style={{ float: "right" }}>
                        <div
                          style={{
                            float: "right",
                            backgroundColor: "#3967AA",
                            width: "10px",
                            height: "10px",
                            borderRadius: "50%",
                            margin: "5px",
                          }}
                        ></div>
                      </Col>
                    </Row>
                  </CardHeader>
                </Card>
              </Col>
              <Col className="ml-center" md="5">
                <Card
                  className="card-chart"
                  style={{
                    background:
                      "linear-gradient(180deg, rgba(255,255,255,1) 30%, rgba(228,237,247,1) 61%, rgba(216,229,244,1) 69%, rgba(210,225,242,1) 79%, rgba(197,216,238,1) 87%, rgba(150,183,224,1) 100%, rgba(0,80,179,1) 100%)",
                  }}
                >
                  <CardHeader
                    style={{ border: "1px grey solid", borderRadius: "7px" }}
                  >
                    <CardBody style={{ margin: "10px" }}>
                      <Row>
                        <Col>
                          <img
                            alt="icono"
                            src={icono6}
                            style={{ width: "40%" }}
                          />
                        </Col>
                        <Col>
                          <h4>Menor nivel dinamico pozo, semana anterior </h4>
                        </Col>
                      </Row>
                      <Row>
                        <Col></Col>
                        <Col>
                          <div>
                            {selected_sensor.token_service === "32ae0a00-7374-46e8-bc5c-e085714748d7" && 
                              <h4>14.2</h4>
                            }
                            {selected_sensor.token_service == "867f9225-24f2-487d-bf28-c2ccd0e662bc" && 
                               <h4> 0.0 (mtrs)</h4>	
                            }

                          </div>
                        </Col>
                        <Col>
                          {user.username === "pozos_iansa" ? (
                            <h4>2022-10-15</h4>
                          ) : (
                            <h4>2022-10-08</h4>
                          )}
                        </Col>
                      </Row>
                    </CardBody>
                    <Row>
                      <Col style={{ float: "right" }}>
                        <div
                          style={{
                            float: "right",
                            backgroundColor: "#3967AA",
                            width: "10px",
                            height: "10px",
                            borderRadius: "50%",
                            margin: "5px",
                          }}
                        ></div>
                      </Col>
                    </Row>
                  </CardHeader>
                </Card>
              </Col>
              <Col className="ml-center" md="5">
                <Card
                  className="card-chart"
                  style={{
                    background: !selected_sensor.d6
                      ? "linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,1) 78%, rgba(184,184,184,1) 100%)"
                      : "linear-gradient(180deg, rgba(255,255,255,1) 30%, rgba(228,237,247,1) 61%, rgba(216,229,244,1) 69%, rgba(210,225,242,1) 79%, rgba(197,216,238,1) 87%, rgba(150,183,224,1) 100%, rgba(0,80,179,1) 100%)",
                  }}
                >
                  <CardHeader
                    style={{
                      border: !selected_sensor
                        ? "1px grey solid"
                        : "1px rgb(57, 103, 170) solid",
                      borderRadius: "7px",
                    }}
                  >
                    <CardBody style={{ margin: "10px" }}>
                      <Row>
                        <Col>
                          <img
                            alt="icono"
                            src={!selected_sensor.d6 ? icono2 : icono7}
                            style={{ width: "40%" }}
                          />
                        </Col>
                        <Col>
                          <h4>Tiempo de operación bomba</h4>
                        </Col>
                      </Row>
                      <Row>
                        <Col></Col>
                        <Col>
                          <div>
                            <h4>
                              {selected_sensor.d6 && (
                                <>
                                  {parseFloat(
                                    accTotal /
                                      selected_sensor.scale /
                                      parseFloat(selected_sensor.d6)
                                  ).toFixed(2)}
                                </>
                              )}{" "}
                              hrs
                            </h4>
                          </div>
                        </Col>
                      </Row>
                    </CardBody>
                    <Row>
                      <Col style={{ float: "right" }}>
                        <div
                          style={{
                            float: "right",
                            backgroundColor: !selected_sensor.d6
                              ? "grey"
                              : "rgb(57, 103, 170)",
                            width: "10px",
                            height: "10px",
                            borderRadius: "50%",
                            margin: "5px",
                          }}
                        ></div>
                      </Col>
                    </Row>
                  </CardHeader>
                </Card>
              </Col>
              <Col className="ml-center" md="5">
                <Card
                  className="card-chart"
                  style={{
                    background:
                       "linear-gradient(180deg, rgba(255,255,255,1) 30%, rgba(228,237,247,1) 61%, rgba(216,229,244,1) 69%, rgba(210,225,242,1) 79%, rgba(197,216,238,1) 87%, rgba(150,183,224,1) 100%, rgba(0,80,179,1) 100%)"
                  }}
                >
                  <CardHeader
                    style={{
                      border: selected_sensor.d6
                        ? "1px grey solid"
                        : "1px solid rgb(57, 103, 170)",
                      borderRadius: "7px",
                    }}
                  >
                    <CardBody style={{ margin: "10px" }}>
                      <Row>
                        <Col>
                          <img
                            alt="icono"
                            src={icono6}
                            style={{ width: "40%" }}
                          />
                        </Col>
                        <Col>
                          <h4>Porcentaje de perdida ultimo mes</h4>
                        </Col>
                      </Row>
                      <Row>
                        <Col></Col>
                        <Col>
                          <div>
                            <h4>49% (JUNIO)</h4>
                          </div>
                        </Col>
                      </Row>
                    </CardBody>
                    <Row>
                      <Col style={{ float: "right" }}>
                        <div
                          style={{
                            float: "right",
                            backgroundColor: "rgb(57, 103, 170)",
                            width: "10px",
                            height: "10px",
                            borderRadius: "50%",
                            margin: "5px",
                          }}
                        ></div>
                      </Col>
                    </Row>
                  </CardHeader>
                </Card>
              </Col>
            </Row>
          </>
        ) : (
          <Row className="mt-5">
            {stat1 && (
              <Col className="ml-center" md="5">
                <Card
                  className="card-chart"
                  style={{
                    background:
                      "linear-gradient(180deg, rgba(255,255,255,1) 30%, rgba(228,237,247,1) 61%, rgba(216,229,244,1) 69%, rgba(210,225,242,1) 79%, rgba(197,216,238,1) 87%, rgba(150,183,224,1) 100%, rgba(0,80,179,1) 100%)",
                  }}
                >
                  <CardHeader
                    style={{ border: "1px #3967AA solid", borderRadius: "7px" }}
                  >
                    <CardBody style={{ margin: "10px" }}>
                      <Row>
                        <Col>
                          <img
                            alt="icono"
                            src={icono6}
                            style={{ width: "40%" }}
                          />
                        </Col>
                        <Col>
                          <h4>Promedio de consumo diario</h4>
                        </Col>
                      </Row>
                      <Row>
                        <Col></Col>
                        {valueMax ? (
                          <Col>
                            <div>
                              <h4>
                                {parseFloat(
                                  valueMax.value / user.profile_data.scale
                                ).toFixed(1)}{" "}
                                (m3)
                              </h4>
                            </div>
                          </Col>
                        ) : (
                          <Col>
                            <h4>CARGANDO DATOS...</h4>
                          </Col>
                        )}
                      </Row>
                    </CardBody>
                    <Row>
                      <Col style={{ float: "right" }}>
                        <div
                          style={{
                            float: "right",
                            backgroundColor: "#3967AA",
                            width: "10px",
                            height: "10px",
                            borderRadius: "50%",
                            margin: "5px",
                          }}
                        ></div>
                      </Col>
                    </Row>
                  </CardHeader>
                </Card>
              </Col>
            )}
            {stat2 && (
              <Col className="ml-center" md="5">
                <Card
                  className="card-chart"
                  style={{
                    background:
                      "linear-gradient(180deg, rgba(255,255,255,1) 30%, rgba(228,237,247,1) 61%, rgba(216,229,244,1) 69%, rgba(210,225,242,1) 79%, rgba(197,216,238,1) 87%, rgba(150,183,224,1) 100%, rgba(0,80,179,1) 100%)",
                  }}
                >
                  <CardHeader
                    style={{ border: "1px #3967AA solid", borderRadius: "7px" }}
                  >
                    <CardBody style={{ margin: "10px" }}>
                      <Row>
                        <Col>
                          <img
                            alt="icono"
                            src={icono1}
                            style={{ width: "40%" }}
                          />
                        </Col>
                        <Col>
                          <h4>Cantidad de estanques llenados</h4>
                        </Col>
                      </Row>
                      <Row>
                        <Col></Col>
                        {statElement ? (
                          <Col>
                            <div>
                              <h4>
                                {" "}
                                {parseFloat(
                                  statElement.production /
                                    statElement.constant_a /
                                    31 +
                                    1
                                ).toFixed(1)}
                                (m3)
                              </h4>
                            </div>
                          </Col>
                        ) : (
                          <Col>
                            <h4>CARGANDO DATOS...</h4>
                          </Col>
                        )}
                      </Row>
                    </CardBody>
                    <Row>
                      <Col style={{ float: "right" }}>
                        <div
                          style={{
                            float: "right",
                            backgroundColor: "#3967AA",
                            width: "10px",
                            height: "10px",
                            borderRadius: "50%",
                            margin: "5px",
                          }}
                        ></div>
                      </Col>
                    </Row>
                  </CardHeader>
                </Card>
              </Col>
            )}
            {stat3 && (
              <Col className="ml-center" md="5">
                <Card
                  className="card-chart"
                  style={{
                    background:
                      "linear-gradient(180deg, rgba(255,255,255,1) 30%, rgba(228,237,247,1) 61%, rgba(216,229,244,1) 69%, rgba(210,225,242,1) 79%, rgba(197,216,238,1) 87%, rgba(150,183,224,1) 100%, rgba(0,80,179,1) 100%)",
                  }}
                >
                  <CardHeader
                    style={{ border: "1px #3967AA solid", borderRadius: "7px" }}
                  >
                    <CardBody style={{ margin: "10px" }}>
                      <Row>
                        <Col>
                          <img
                            alt="icono"
                            src={icono5}
                            style={{ width: "40%" }}
                          />
                        </Col>
                        <Col>
                          <h4>Perdidas de facturación</h4>
                        </Col>
                      </Row>
                      <Row>
                        <Col></Col>
                        {statElement ? (
                          <Col>
                            <div>
                              <h4>
                                {statElement.production - statElement.billing}{" "}
                                (m3)
                              </h4>
                            </div>
                          </Col>
                        ) : (
                          <Col>
                            <h4>CARGANDO DATOS...</h4>
                          </Col>
                        )}
                      </Row>
                    </CardBody>
                    <Row>
                      <Col style={{ float: "right" }}>
                        <div
                          style={{
                            float: "right",
                            backgroundColor: "#3967AA",
                            width: "10px",
                            height: "10px",
                            borderRadius: "50%",
                            margin: "5px",
                          }}
                        ></div>
                      </Col>
                    </Row>
                  </CardHeader>
                </Card>
              </Col>
            )}

            <Col className="ml-center" md="5">
              <Card
                className="card-chart"
                style={{
                  background:
                    "linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,1) 78%, rgba(184,184,184,1) 100%)",
                }}
              >
                <CardHeader
                  style={{ border: "1px solid", borderRadius: "7px" }}
                >
                  <CardBody style={{ margin: "10px" }}>
                    <Row>
                      <Col>
                        <img
                          alt="icono"
                          src={icono2}
                          style={{ width: "40%" }}
                        />
                      </Col>
                      <Col>
                        <h4 style={{ color: "grey" }}>Bomba pozo profundo</h4>
                      </Col>
                    </Row>

                    <Row>
                      <Col></Col>
                      <Col>
                        <h4 style={{ color: "grey" }}>Mantenimiento: x días</h4>
                      </Col>
                    </Row>
                  </CardBody>
                  <Row>
                    <Col style={{ float: "right" }}>
                      <div
                        style={{
                          float: "right",
                          backgroundColor: "grey",
                          width: "10px",
                          height: "10px",
                          borderRadius: "50%",
                          margin: "5px",
                        }}
                      ></div>
                    </Col>
                  </Row>
                </CardHeader>
              </Card>
            </Col>
            <Col className="ml-center" md="5">
              <Card
                className="card-chart"
                style={{
                  background:
                    "linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,1) 78%, rgba(184,184,184,1) 100%)",
                }}
              >
                <CardHeader
                  style={{ border: "1px solid", borderRadius: "7px" }}
                >
                  <CardBody style={{ margin: "10px" }}>
                    <Row>
                      <Col>
                        <img
                          alt="icono"
                          src={icono3}
                          style={{ width: "40%" }}
                        />
                      </Col>
                      <Col>
                        <h4 style={{ color: "grey" }}>Recuperación de pozo</h4>
                      </Col>
                    </Row>
                    <Row>
                      <Col></Col>
                      <Col>
                        <h4 style={{ color: "grey" }}>0000 seg</h4>
                      </Col>
                    </Row>
                  </CardBody>
                  <Row>
                    <Col style={{ float: "right" }}>
                      <div
                        style={{
                          float: "right",
                          backgroundColor: "grey",
                          width: "10px",
                          height: "10px",
                          borderRadius: "50%",
                          margin: "5px",
                        }}
                      ></div>
                    </Col>
                  </Row>
                </CardHeader>
              </Card>
            </Col>
            <Col className="ml-center" md="5">
              <Card
                className="card-chart"
                style={{
                  background:
                    "linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,1) 78%, rgba(184,184,184,1) 100%)",
                }}
              >
                <CardHeader
                  style={{ border: "1px solid", borderRadius: "7px" }}
                >
                  <CardBody style={{ margin: "10px" }}>
                    <Row>
                      <Col>
                        <img
                          alt="icono"
                          src={icono4}
                          style={{ width: "40%" }}
                        />
                      </Col>
                      <Col>
                        <h4 style={{ color: "grey" }}>
                          Factibilidad Nuevos Arranques
                        </h4>
                      </Col>
                    </Row>
                    <Row>
                      <Col></Col>
                      <Col>
                        <h4 style={{ color: "grey" }}>0000</h4>
                      </Col>
                    </Row>
                  </CardBody>
                  <Row>
                    <Col style={{ float: "right" }}>
                      <div
                        style={{
                          float: "right",
                          backgroundColor: "grey",
                          width: "10px",
                          height: "10px",
                          borderRadius: "50%",
                          margin: "5px",
                        }}
                      ></div>
                    </Col>
                  </Row>
                </CardHeader>
              </Card>
            </Col>
            
          </Row>
        )}
        <Row >
          <Col className="ml-center" md="5">
                <Card
                  className="card-chart"
                  style={{
                    background:
                       "linear-gradient(180deg, rgba(255,255,255,1) 30%, rgba(228,237,247,1) 61%, rgba(216,229,244,1) 69%, rgba(210,225,242,1) 79%, rgba(197,216,238,1) 87%, rgba(150,183,224,1) 100%, rgba(0,80,179,1) 100%)"
                  }}
                >
                  <CardHeader
                    style={{
                      border: selected_sensor.d6
                        ? "1px grey solid"
                        : "1px solid rgb(57, 103, 170)",
                      borderRadius: "7px",
                    }}
                  >
                    <CardBody style={{ margin: "10px" }}>
                      <Row>
                        <Col>
                          <img
                            alt="icono"
                            src={icono6}
                            style={{ width: "40%" }}
                          />
                        </Col>
                        <Col>
                          <h4>Consumo energetico, bomba mes anterior</h4>
                        </Col>
                      </Row>
                      <Row>
                        <Col></Col>
                        <Col>
                          <div>
                            <h4>$ 50.820</h4>
                          </div>
                        </Col>
                      </Row>
                    </CardBody>
                    <Row>
                      <Col style={{ float: "right" }}>
                        <div
                          style={{
                            float: "right",
                            backgroundColor: "rgb(57, 103, 170)",
                            width: "10px",
                            height: "10px",
                            borderRadius: "50%",
                            margin: "5px",
                          }}
                        ></div>
                      </Col>
                    </Row>
                  </CardHeader>
                </Card>
              </Col>
<Col className="ml-center" md="5">
                <Card
                  className="card-chart"
                  style={{
                    background:
                       "linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,1) 78%, rgba(184,184,184,1) 100%)"
                  }}
                >
                  <CardHeader
                    style={{
                      border: selected_sensor.d6
                        ? "1px grey solid"
                        : "1px grey",
                      borderRadius: "7px",
                    }}
                  >
                    <CardBody style={{ margin: "10px" }}>
                      <Row>
                        <Col>
                          <img
                            alt="icono"
                            src={icono4}
                            style={{ width: "40%" }}
                          />
                        </Col>
                        <Col>
                          <h4>Disponibilidad de agua para nuevos arranques</h4>
                        </Col>
                      </Row>
                      <Row>
                        <Col></Col>
                        <Col>
                          <div>
                            <h4>x</h4>
                          </div>
                        </Col>
                      </Row>
                    </CardBody>
                    <Row>
                      <Col style={{ float: "right" }}>
                        <div
                          style={{
                            float: "right",
                            backgroundColor: "grey",
                            width: "10px",
                            height: "10px",
                            borderRadius: "50%",
                            margin: "5px",
                          }}
                        ></div>
                      </Col>
                    </Row>
                  </CardHeader>
                </Card>
              </Col>

        </Row>
      </div>
    </>
  );
};

const styles = {
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

export default Charts2;
