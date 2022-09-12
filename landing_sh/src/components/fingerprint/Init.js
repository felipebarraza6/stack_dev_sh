import React, {useEffect, useState} from 'react'
import { Row,Col, Typography, Input, Card } from 'antd'
import Navigate from './Navigate'
import StatusLine from './StatusLine'
import {callbacks} from '../../api/endpoints'
import FormFields from './FormFields'
import img1 from '../../assets/images/CA.png'
import img2 from '../../assets/images/agencia_sus.png'


  const Init = ({ match }) => {

    const initialState = {
      id_fingerprint: match.params.id,
      data_fingerprint: null,
      fields: null,
      section_selected: null,
    }

    const [state, setState] = useState(initialState)

    const getData = async()=> {
      const rq = await callbacks.fingerprint.retrieve(state.id_fingerprint)
        .then((x) => setState({ ...state, data_fingerprint: x.data }))
    }

    useEffect(()=> {
      getData()
    }, [])


    return(<>
      <Col span={6} style={styles.container}>        
        {state.data_fingerprint && <>
          <Typography.Title level={4}>{state.data_fingerprint.title} (#{state.data_fingerprint.id})</Typography.Title>
          <Navigate elements={state.data_fingerprint.modules} setState={setState} state={state} />          
        </>}
        <Navigate />
      </Col>
      <Col span={18} style={styles.nav}>
        {state.section_selected ?
          <StatusLine  section={state.section_selected} />: <>
            {state.data_fingerprint && <div style={{paddingTop:'80px'}}>
              <Typography.Title level={2}>{state.data_fingerprint.title_presentation}</Typography.Title>
              <Typography.Title level={5}>{state.data_fingerprint.description_presentation}</Typography.Title>
              <Row style={{margin:'60px'}} align="center" justify="center">
                <Col span={8}>
                  <img src={img1} width="150px" />
                </Col>
                  <Col span={8}>
                  <img src={img2} width="150px" />
                </Col>
                <Col span={8}>
                  <Card hoverable>
                    <Typography.Title level={4}>SOPORTE</Typography.Title>
                    <Typography.Paragraph>
                      Encargado de desarrollo: <br/>Felipe Barraza
                    </Typography.Paragraph>
                    <Typography.Paragraph>
                      Correo: <br/>felipe.barraza@smarthydro.cl
                    </Typography.Paragraph>
                    <Typography.Paragraph>
                      WhatsApp: <br/>+56 9 3393 2112
                    </Typography.Paragraph>
                  </Card>
                </Col>
              </Row>
            </div>} 
          </>}
        <Row style={styles.rowContainer}>
          <FormFields fields={state.fields} section={state.section_selected} />          
        </Row>
      </Col>
    </>)
}

const styles = {
  container: {
    padding: '20px'
  },
  nav:{
    backgroundColor: 'white',
    padding: '20px'
  },
  rowContainer: {
    marginTop: '20px'
  }
}


export default Init
