import React, { useEffect,useContext, useState} from 'react'
import { Row, Col, Table, Typography, Button, Card } from 'antd'
import sh from '../../api/sh/endpoints'
import { FileImageOutlined } from '@ant-design/icons'
import { AppContext } from '../../App'

const {Title}=Typography

const Dga = () => {
    const {state} =useContext(AppContext)
    const [data,setData]=useState([])
    console.log(state)
    const getData = async() => {
        const rq = await sh.get_data_sh(state.selected_profile.id).then((x)=>console.log(x.results[0]))
    }

    useEffect(()=>{
        getData()
    }, [])

    return(
<Card style={{borderRadius:'20px', paddingTop:'50px', paddingBottom:'100px'}} hoverable><Row>
        <Col span={24}>
            <Title level={2}>Datos enviados a DGA <span style={{fontSize:'20px'}}>(últimas 24 horas)</span></Title>
        </Col>
        <Col span={12} style={{padding:'20px'}}>
            <Table style={{borderRadius:'20px'}} bordered size='small' dataSource={data} columns={[
                {title:'Fecha'},
                {title:'Caulda(lt)'},
                {title:'Acumulado(m³)'},
                {title:'Nivel(m)'}
                ]} />
        </Col>
        <Col span={12}>
                <center><FileImageOutlined style={{fontWeight:'100',fontSize:'150px', textAlign:'center', color: '#1f3461'}} /><br/><br/>
                <Title level={4}>CODIGO DE OBRA</Title>
                <Button style={{borderRadius:'10px', backgroundColor:'#1f3461', color:'white'}} disabled>Ir a mi Dga</Button></center>
        </Col>
        </Row>
        </Card>
    )

}


export default Dga