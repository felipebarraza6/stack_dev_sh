import React, { useState } from 'react'
import { Row, Col, Typography } from 'antd'
import ListElements from './ListElements'
import FormElement from './FormElement'


const { Title } = Typography

const ConfigElements = () => {

    const [count, setCount] = useState(0)
    const [selectElement, setSelectElement] = useState(null)
    //const [select]
    console.log(selectElement)

    return(<Row>
        <Col span={24}>
            <Title level={3}>Configuración de entradas en modulo de proyectos</Title>
        </Col>
        <Col span={16}>
            <ListElements setSelectElement={setSelectElement} count={count} setCount={setCount} />
        </Col>
        <Col span={8}>            
            <FormElement selectElement={selectElement} setSelectElement={setSelectElement} count={count} setCount={setCount} />
        </Col>
    </Row>)

}


export default ConfigElements