import React, { useEffect, useState } from 'react'
import { Row, Col, Typography, 
        Table } from 'antd'
import { callbacks } from '../api/endpoints'
const { Title } = Typography


const Inscribed = () => {

    const [elements, setElements] = useState([])
    const [count, setCount] = useState(0)

    useEffect(() => {
        const getItems = async() => {
            const request = await callbacks.list()            
            setElements(request.data.results)
            setCount(request.data.count)
            console.log(request)
        }

        getItems()

    }, [])

    const columns = [
        {
          title: 'Nombre',
          dataIndex: 'name',
          key: 'name',
        },        
        {
          title: 'Organización',
          dataIndex: 'enterprise',
          key: 'enterprise',
        },
        {
            title: 'Comuna',
            dataIndex: 'commune',
            key: 'commune',
        },
        
      ]

    

    console.log(count)

    return(<Row style={styles.container} align="middle">
        <Col  xs={24} lg={12} md={12}>
            <Title level={2} style={styles.title}>Nos sumamos a crear el ecosistema de emprendimiento que necesita Ñuble</Title>
            <Title level={2} style={styles.title}>Ya somos {count} inscrit@s </Title>
        </Col>
        <Col  xs={24} lg={12} md={12}>
            <Table  bordered columns={columns} dataSource={elements} pagination= {{
                pageSize:5
            }} />
        </Col>
    </Row>)

}


const styles = {
    title: {
        textAlign: 'center',
    
        paddingLeft:'30ox',
        paddingRight:'30px'
    },
    container: {
        padding: '50px',
        backgroundColor: 'white'
    }
}


export default Inscribed