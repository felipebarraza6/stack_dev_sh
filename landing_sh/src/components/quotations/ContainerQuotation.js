import React, { useContext } from 'react'
import { QuotationContext } from '../../containers/QuotationExternalClients'
import FormClientExternal from '../external_clients/FormClientExternal'
import AddWell from '../quotations/AddWell'
import TimeLineProcess from './TimeLineProcess'
import { Row, Col, Typography } from 'antd'

const { Title } = Typography

const ContainerQuotation = () => {
  
  const { state, dispatch } = useContext(QuotationContext)

  return(<Row >
        <Col span={4}>
          <TimeLineProcess />
        </Col>
        <Col span={20}>
        <Row justify="space-around" align="middle" style={styles.container}>
          {state.steps.current === 0 && <Col>
            <Title level={3}>Primero debes ingresar tus datos de contacto...</Title>
            <FormClientExternal />
          </Col>}        
          {state.steps.current === 1 && <Col>
              <AddWell />
          </Col>}
        </Row>
        </Col>
    </Row>)

}

const styles = {
  container: {    
    paddingTop: '4%',
    paddingBottom: '4%',
      
  },
}


export default ContainerQuotation
