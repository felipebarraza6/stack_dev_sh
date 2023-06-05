import React from 'react'
import { Descriptions, Typography, Button } from 'antd'
import ModalEnterprise from '../../clients/ModalEnterprise'
import { BuildOutlined } from '@ant-design/icons'

const { Item } = Descriptions
const { Text, Title } = Typography

const GeneralProjectInfo = ({ project }) => {

  return(
    <Descriptions size='small' layout="vertical" bordered title={<Title level={3}>{project.name}</Title>} >
      <Item label='Cliente'>
        <Button icon={<BuildOutlined />} type='primary' onClick={()=> ModalEnterprise(project.client)}>
          {project.client.name}
        </Button>
      </Item>
      <Item label='Codigo'>
        <Text mark>
          {project.code_internal}
        </Text>
      </Item>
      <Item label='Fecha de creación'>
        <Text mark>
          {project.created.slice(0,10)}
        </Text>
      </Item>
      <Item label='Descripción'>
        {project.description}
      </Item>
    </Descriptions>
  )

}


export default GeneralProjectInfo
