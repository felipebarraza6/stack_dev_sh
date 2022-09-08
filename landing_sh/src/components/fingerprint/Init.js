import React, {useEffect, useState} from 'react'
import { Row,Col, Typography, Input } from 'antd'
import Navigate from './Navigate'
import StatusLine from './StatusLine'
import {callbacks} from '../../api/endpoints'
import FormFields from './FormFields'


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
        <StatusLine  section={state.section_selected} />
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