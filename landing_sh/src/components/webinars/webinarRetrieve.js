import React, { useState, useEffect } from 'react'
import { Row, Col, Card, Typography, 
        Button, Modal } from 'antd'
import { callbacks } from '../../api/endpoints'
import FormClientExternal from '../external_clients/FormClientExternal'
const { Title, Paragraph, Text } = Typography


const WebinarRetrieve = ({ match }) => {
  
  console.log(match.params.id)

  const initialStateData = {
    id: match.params.id,
    data: {}
  }

  const [widths, setWidths] = useState(null)
  const [stateData, setStateData] = useState(initialStateData)
  const [isStatusSub, setStatusSub] = useState(false)

  function openModalFormExternalClient(){
    Modal.info({ content: <Row><FormClientExternal isModal={true} setStatusSub={setStatusSub} /></Row>, okText:'Cerrar' })
  }

  async function getData(id){
    const rq = await callbacks.webinar.retrieve(id).then((res)=> {
      setStateData({...stateData, data: res.data})
    }).catch((e)=> console.log(e))
    return rq
  }

  useEffect(() =>{
    setWidths(window.innerWidth)
    getData(stateData.id)
  }, [])

  return(<>
          {widths > 800 &&  
            <Col xl={12} lg={12}>
              <img src={stateData.data.wallpaper_img} style={styles.wallImg} alt='wallpaper' />
            </Col>}
          <Col lg={12} xs={24} xl={12}>
              <Card>
                <Row>
                  <Col lg={10} xs={8} xl={10}>
                    <img src={stateData.data.img_present} style={styles.avatarImg} alt='avatar' />
                    <Paragraph strong>{stateData.data.present}</Paragraph>
                    <Paragraph style={styles.chargeTxt}>{stateData.data.charge_present}</Paragraph>
                  </Col>
                  <Col lg={12} xl={12} xs={16} style={styles.colInfo}>
                    <Title level={4}>{stateData.data.title}</Title>
                    <Title level={5}>{stateData.data.subtitule}</Title>
                    <Paragraph align='justify'>{stateData.data.description}</Paragraph>
                    <Text mark>{stateData.data.txt_date}</Text><br /><br />
                    <Paragraph style={styles.txtInfo}>
                      El registro e ingreso al Webinar, se habilitara 30 minutos previos a la fecha y hora de inicio programada.
                    </Paragraph>                                  
                    {isStatusSub ? <>
                      <Button type='primary' onClick={()=> window.open(stateData.data.link_meet)}>INGRESAR</Button>
                      </>:
                    <Button type='primary' disabled={stateData.data.is_active} onClick={openModalFormExternalClient}>
                      REGISTRARSE PARA INGRESAR
                    </Button>}
                  </Col>
                </Row>
              </Card>
          </Col>      
  </>)

}

const styles = {
  txtInfo: {
    color: 'grey'
  },
  colInfo: {
    backgroundColor: 'white'
  },
  chargeTxt: {
    paddingRight: '20px'
  },
  wallImg: {
    width: '100%',
    marginTop: '15px',
    opacity: '0.7',
  },
  avatarImg: {
    width: '80%',
    border: '3px solid #1890ff',
    borderRadius: '8px',
    marginTop: '0px',
    marginBottom: '20px'
  }
}

export default WebinarRetrieve
