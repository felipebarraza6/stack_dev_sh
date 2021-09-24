import React from 'react'

import { Col, Statistic } from 'antd'
import { TeamOutlined } from '@ant-design/icons'

const Totals = (attr) =>{
    
    return (        
        <React.Fragment>                                                
            <Col span={8}>
                <Statistic style={{backgroundColor: 'white', marginRight:'30px', padding:'20px'}} 
                    title="Personas Totales"
                    value={attr.data.employess.count}                    
                    valueStyle={{ color: '#1890ff' }}
                    prefix={<TeamOutlined />}
                />
            </Col>
            <Col span={8}>
               <Statistic style={{backgroundColor: 'white', marginRight:'30px', padding:'20px'}} 
                    title="Personas Activas"
                    value={attr.data.employess_actives.count}
                    valueStyle={{ color: 'green' }}
                    prefix={<TeamOutlined />}
                />
            </Col>
            <Col span={8}>
               <Statistic style={{backgroundColor: 'white', marginRight:'30px', padding:'20px'}} 
                    title="Personas Inactivas"
                    value={attr.data.employess_inactives.count}            
                    valueStyle={{ color: 'red' }}
                    prefix={<TeamOutlined />}
                />
            </Col>            
        </React.Fragment>
    )
}

export default Totals