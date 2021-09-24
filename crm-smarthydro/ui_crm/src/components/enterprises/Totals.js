import React from 'react'

import { Col, Statistic } from 'antd'
import { BuildOutlined } from '@ant-design/icons'


const Totals = (total) =>{
    
    return (
        <React.Fragment>                                    
            <Col span={8}>
                <Statistic style={{backgroundColor: 'white', marginRight:'30px', padding:'20px'}} 
                    title="Empresas Totales"
                    value={total.data.enterprises}            
                    valueStyle={{ color: '#1890ff' }}
                    prefix={<BuildOutlined />}
                />
            </Col>
            <Col span={8}>
               <Statistic style={{backgroundColor: 'white', marginRight:'30px', padding:'20px'}} 
                    title="Empresas Activas"
                    value={total.data.enterprises_actives}        
                    valueStyle={{ color: 'green' }}
                    prefix={<BuildOutlined />}
                />
            </Col>
            <Col span={8}>
               <Statistic style={{backgroundColor: 'white', marginRight:'30px', padding:'20px'}} 
                    title="Empresas Inactivas"
                    value={total.data.enterprises_inactive}           
                    valueStyle={{ color: 'red' }}
                    prefix={<BuildOutlined />}
                />
            </Col>            
        </React.Fragment>
    )
}

export default Totals