//React
import React from 'react'

//Ant Design
import { Row, Col, Card, Statistic } from 'antd'

import { AlertTwoTone, WarningTwoTone,
    CheckCircleTwoTone, BookTwoTone } from '@ant-design/icons'

 const Totals = ({ totals }) => {
     
    return(
        <React.Fragment>
            {totals &&
            <Row>
                <Col span={24}>
                    <Card>
                        <Card.Grid style={{height:'100px', width:'25%'}}>
                            <Row>
                                <Col style={{margin:'20px'}}>
                                    <BookTwoTone style={{fontSize:'40px', marginLeft:'20%'}} />
                                </Col>
                                <Col >
                                    <Statistic title="TOTAL" value={totals.totals.data.count} />
                                </Col>
                            </Row>
                        </Card.Grid>
                        <Card.Grid style={{height:'100px', width:'25%'}}>
                            <Row>
                                <Col style={{margin:'20px'}}>
                                    <AlertTwoTone style={{fontSize:'40px', marginLeft:'20%'}} />
                                </Col>
                                <Col >
                                    <Statistic title="ACTIVAS" value={totals.actives.data.count} />
                                </Col>
                            </Row>
                        </Card.Grid>
                        <Card.Grid style={{height:'100px', width:'25%'}}>
                            <Row>
                                <Col style={{margin:'20px'}}>
                                    <WarningTwoTone style={{fontSize:'40px', marginLeft:'20%'}} />
                                </Col>
                                <Col >
                                    <Statistic title="PRIORIDAD" value={totals.priority.data.count} />
                                </Col>
                            </Row>
                        </Card.Grid>
                        <Card.Grid style={{height:'100px', width:'25%'}}>
                            <Row>
                                <Col style={{margin:'20px'}}>
                                    <CheckCircleTwoTone style={{fontSize:'40px', marginLeft:'20%'}} />
                                </Col>
                                <Col >
                                    <Statistic title="COMPLETADAS" value={totals.completes.data.count} />
                                </Col>
                            </Row>
                        </Card.Grid>                        
                    </Card>
                </Col>
            </Row>
            }
        </React.Fragment>
    )

 }

 export default Totals