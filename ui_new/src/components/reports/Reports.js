import React, { useContext } from 'react'

import { Row, Col, Typography, Table } from 'antd'
import { AppContext } from '../../App'

const { Title } = Typography

const Reports = () => {

    const { state } = useContext(AppContext)
    console.log(state.selected_profile.persons)
    return(<Row style={{padding:'20px'}}>
        <Col span={24}>
                <Title level={2}>Listado de usuarios autorizados</Title>
            </Col>
            <Col span={24} style={{marginTop:'10px', marginBottom:'0px', }}>
                <Table pagination={false} bordered columns={[
                    {title:'#', dataIndex:'id'},                        
                    {title:'Nombre', dataIndex:'name'},
                    {title:'Email', dataIndex: 'email'},
                    {title:'Teléfono', dataIndex: 'phone'},
                ]} dataSource = {state.selected_profile.persons} />
            </Col>                
    </Row>)
}


export default Reports