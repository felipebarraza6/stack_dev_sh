import React, { useContext } from 'react'
import { QuotationContext } from '../../containers/Quotation'
import FormClientExternal from '../external_clients/FormClientExternal'
import Well from './well/Well'
import TimeLineProcess from './TimeLineProcess'
import ImageOrFinish from './well/ImageOrFinish'
import { Row, Col, Typography } from 'antd'

const { Title } = Typography

const ContainerQuotation = () => {
  
  const { state, dispatch } = useContext(QuotationContext)

  const styles = {
    container: {    
      paddingTop: state.steps.current===0 ? '4%':'1%',
      margin:window.innerWidth > 800 ? '0px':'10px'
    },
  }

  return(<Row>
        {window.innerWidth  > 800 && <Col span={4}>
          <TimeLineProcess />
        </Col>}        
        <Col span={window.innerWidth > 800 ? 20:24}>
        <Row  style={styles.container}>
          {state.steps.current === 0 && <Col>
            <Title level={3}>Primero debes ingresar tus datos de contacto...</Title>
            <FormClientExternal />
          </Col>}        
          {state.steps.current === 1 && <Col span={24}>
            <Well />
          </Col>}
          {state.steps.current === 2 && <Col span={24}>
            <ImageOrFinish />
          </Col>}
          {state.steps.current === 4 && <Col span={24}>
            <ImageOrFinish />
          </Col>}
        </Row>
        </Col>
    </Row>)

}




export default ContainerQuotation
