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

    const getDataSh= async() =>{
        const rq = await sh.get_data_sh(state.selected_profile.id).then((r)=>{
            let today = new Date(); 
            let year = today.getFullYear();
            let month = today.getMonth() + 1;
            let day = today.getDate()-1;
            let formattedDate = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
            console.log(formattedDate);
          setData([{
            nivel: r.results[0].nivel ? r.results[0].nivel:0,
            caudal: r.results[0].flow ? r.results[0].flow:0,
            acumulado: r.results[0].total ? r.results[0].total:0,
            fecha: formattedDate
          }])
          
        })
      }

    useEffect(()=>{
        getData()
        getDataSh()
    }, [state.selected_profile])

    return(
<Card style={{borderRadius:'20px', paddingTop:'50px', paddingBottom:'100px'}} hoverable><Row>
        <Col span={24}>
            <Title level={2}>Datos enviados a DGA <span style={{fontSize:'20px'}}></span></Title>
        </Col>
        <Col span={12} style={{padding:'20px'}}>
            <Table style={{borderRadius:'20px'}} bordered size='small' dataSource={data} columns={[
                {title:'Fecha', dataIndex:'fecha'},
                {title:'Caulda(lt)', dataIndex:'caudal'},
                {title:'Acumulado(m³)', dataIndex:'acumulado'},
                {title:'Nivel(m)', dataIndex:'nivel'}
                ]} />
        </Col>
        <Col span={12}>
                <center>
                {state.selected_profile.qr_dga ? <><img width={'50%'} src={`https://api.smarthydro.cl/${state.selected_profile.qr_dga}`} /><br/><br/></>: <>
                    <FileImageOutlined style={{fontWeight:'100',fontSize:'150px', textAlign:'center', color: '#1f3461'}} /><br/><br/>
                    </>
                }
                <Title level={4}>{state.selected_profile.code_dga_site ? state.selected_profile.code_dga_site:'CÓDIGO DE OBRA'}</Title>
                <Button style={{borderRadius:'10px', backgroundColor:'#1f3461', color:'white'}} disabled>Ir a mi Dga</Button></center>
        </Col>
        </Row>
        </Card>
    )

}


export default Dga