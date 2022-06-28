
import React from 'react'
import { Col, Row, Card,
        Tag, } from 'antd'

const YourData = ({ data }) => {
          return(<>
                <Col style={styles.col_datas} >
                  <Card style={styles.card_general} title='datos generales' bordered hoverable>
                    nombre: <Tag style={styles.tag} color='blue'>{data.general.name}</Tag><br />
                    region: <Tag style={styles.tag}  color='blue'>{data.general.region}</Tag><br />
                    comuna: <Tag style={styles.tag}  color='blue'>{data.general.commune}</Tag><br />
                  </Card>
                </Col>
                <Col style={styles.col_datas}>
                  <Card style={styles.card_contact} title='datos de contacto' bordered hoverable>
                    nombre: <Tag style={styles.tag} color='blue'>{data.contact.name}</Tag><br />
                    correo: <Tag style={styles.tag} color='blue'>{data.contact.mail}</Tag><br />
                    telefono: <Tag style={styles.tag} color='blue'>{data.contact.phone}</Tag><br />
                  </Card>
                </Col>
                <Col style={styles.col_datas}>
                  <Card style={styles.card_tec} title='datos de tecnicos' bordered hoverable>
                      <Col style={styles.col_tech}>
                        resolución: <Tag style={styles.tag} color='blue'>{data.technicians.resolution}</Tag>
                      </Col>
                      <Col style={styles.col_tech}>
                        estandar: <Tag style={styles.tag} color='blue'>{data.technicians.standard}</Tag>
                      </Col>
                      <Col style={styles.col_tech}>
                        fecha vencimiento - instalación: <Tag style={styles.tag} color='blue'>{data.technicians.date_installation}</Tag>
                      </Col>
                      <Col style={styles.col_tech}>
                        fecha vencimiento - transmisión: <Tag style={styles.tag} color='blue'>{data.technicians.date_transmission}</Tag>
                      </Col>
                      <Col style={styles.col_tech}>
                        fecha publicación diario oficial: <Tag style={styles.tag} color='blue'>{data.technicians.date_diary_official}</Tag>
                      </Col>
                  </Card>
                </Col>
          </>)
}


const styles = {
  card_general: {
    width: '300px'
  },
  card_contact: {
    width: '300px'
  },
  card_tec: {
    width: '400px'
  },
  col_datas: {
    padding:'20px',
  },
  col_datas_b: {
    paddingleft: '20px',
    paddingright: '20px',
    marginbottom: '100px',
  },
  col_tech: {
    padding: '3px'
  }, 
  tag: {
    margin: '3px'
  },
  card: {
    width: '300px',
  }
}


export default YourData
