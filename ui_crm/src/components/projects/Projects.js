import React, {useState} from 'react'
import { Row, Col, Typography, 
          Card, Input, Button,
          Table, Select, Descriptions, Modal, Drawer } from 'antd'
import FormProject from './FormProject'
import ListProjects from './ListProjects'

const { Title } = Typography

const Projects = () => {

  const [count, setCount] = useState(0)
  const [selectProject, setSelectProject] = useState(null)

  return(<Row>
          <Col span={24}>
            <Title>Proyectos</Title>
          </Col>
          <Col span={16}>
            <ListProjects setCount={setCount} count={count} setSelectClient={setSelectProject} />
          </Col>          
          <Col span={8}>
            <FormProject selectProject={selectProject} setCount={setCount} count={count} setSelectClient={setSelectProject} />          
          </Col>

    </Row>)
}


export default Projects
