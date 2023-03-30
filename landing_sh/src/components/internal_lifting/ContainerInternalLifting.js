import React, { useContext } from 'react'
import { QuotationContext } from '../../containers/Quotation'
import { InternalLiftingContext } from '../pages/InternalLifting'
import FormClientExternal from '../external_clients/FormClientExternal'
import FormClient from '../external_clients/FormClient'
import Well from './well/Well'
import TimeLineProcess from './TimeLineProcess'
import ImageOrFinish from './well/ImageOrFinish'
import { Row, Col, Typography } from 'antd'

const { Title } = Typography

const ContainerInternalLifting = () => {
  
  const { state, dispatch } = useContext(InternalLiftingContext)

  const styles = {
    container: {    
      paddingTop: state.steps.current===0 ? '4%':'1%',
      margin:window.innerWidth > 800 ? '0px':'10px',
      
    },
  }

  return(<Row justify={'center'} >
      <Col span={24} style={{backgroundColor:'#002c8c', paddingLeft:'10px', paddingTop:'5px'}}>
        <Title style={{color:'white'}} level={window.innerWidth>900?2:4}>App levantamiento de información</Title>
      </Col>
        {window.innerWidth  > 800 && <Col span={4}>
          <TimeLineProcess />
        </Col>}        
        <Col span={window.innerWidth > 800 ? 20:24}>
        <Row justify={'center'} align={'middle'} style={styles.container}>
                  
          {state.steps.current === 0 && <Col span={24}>
            <Well />
          </Col>}
          {state.steps.current === 1 && <Col span={24}>
            <ImageOrFinish />
          </Col>}
          {state.steps.current === 2 && <Col span={24}>
            <ImageOrFinish />
          </Col>}
          {state.steps.current === 3 && <Col xl={10}>
            <FormClient />
          </Col>}
        </Row>
        </Col>
    </Row>)

}




export default ContainerInternalLifting
