import React from 'react'
import { Row, Col } from 'antd'

import HeaderNav from '../components/home/HeaderNav'
import { BrowserRouter, Routes, Route } from "react-router-dom"
import SiderRight from '../components/home/SiderLeft'
import SiderLeft from '../components/home/SiderRight'
import ListWells from '../components/home/ListWells'
import MyWell from '../components/mywell/MyWell'
import MyGraphics from '../components/graphics/MyGraphics'
import Reports from '../components/reports/Reports'
import Indicators from '../components/Indicators/Indicators'

const Home = () => {

    return(<Row>
        <BrowserRouter>
        <Col span={24}>
            <HeaderNav />
        </Col>
        <Col span={24}>
            <Row >
                {window.innerWidth>900 && 
                <Col span={3} style={{padding:'5px'}}>                    
                    <SiderRight />                    
                </Col>}
                <Col span={window.innerWidth > 900? 17:24}>
                    <Row justify='center'>
                        <Col span={24} >
                            <ListWells />
                        </Col>
                        <Col span={24}>
                            <Routes>
                                <Route exact path="/" element={<MyWell />} />
                                <Route exact path="/graficos" element={<MyGraphics />} />
                                <Route exact path="/indicadores" element={<Indicators />} />
                                <Route exact path="/reportes" element={<Reports />} />
                            </Routes>
                        </Col>
                    </Row>                    
                </Col>     
                {window.innerWidth>900 && 
                <Col span={window.innerWidth > 900?4:24} style={{padding:'5px'}}>
                    <SiderLeft />
                </Col>}
            </Row>
        </Col>
        </BrowserRouter>     
    </Row>)
}


export default Home
