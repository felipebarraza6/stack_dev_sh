import React, { useContext, useState } from 'react'

import { Row, Col, Typography, 
      Table, Button } from 'antd'
import { AppContext } from '../../App'

import { CloudDownloadOutlined, LoadingOutlined } from '@ant-design/icons'
import sh from '../../api/sh/endpoints'

const { Title } = Typography

const Reports = () => {

    const { state } = useContext(AppContext)
    const [selectDownload, setSelectDownload] = useState(null)
    

    return(<Row style={{padding:'20px'}}>
        <Col span={24}>
                <Title level={2}>Listado de usuarios autorizados</Title>
            </Col>
            <Col span={24}>
      {state.profile_client.map((x, index)=> {
                return(<Button 
                  onClick={async()=> {

                    setSelectDownload(index)
                    const rq = await sh.downloadFile(x.id, x.title).then((x)=>{
                      setSelectDownload(null)
                    }).catch((x)=> setSelectDownload(null))
                  }}
                  type='primary' style={{margin:'10px', backgroundColor:'#CBCE07', borderColor:'#CBCE07', color:'black', borderRadius:'10px'}} 
                    icon={selectDownload == index ? <LoadingOutlined/>:<CloudDownloadOutlined />} >{x.title}</Button>)
              })}
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
