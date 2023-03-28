import React from 'react'
import { Row, Col, Typography, 
          Card, Input, Button,
          Table, Select, Descriptions, Upload } from 'antd'
import { DownloadOutlined } from '@ant-design/icons'

const { Title } = Typography


const Files = () => {

  return(<Row>
          <Col span={24}>
            <Title>Archivos</Title>
          </Col>
          <Col span={8}>
            <Card title='Archivos por cliente'>
              <Select placeholder='Filtrar por cliente...'></Select>
              <Select placeholder='Tipo de archivo'>
                <Select.Option>Cotización</Select.Option>
              </Select>
              <Descriptions style={{marginTop:'10px'}} title='Cliente #1' bordered hoverable layout='vertical'>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
<Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
<Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
              </Descriptions>
            </Card>
          </Col>
          <Col span={8}>
            <Card title='Archivos por proyecto'>
              <Input placeholder='Codigo proyecto' style={{width:'160px'}} />
              <Select placeholder='Tipo de archivo'>
                <Select.Option>Cotización</Select.Option>
              </Select>
              <Descriptions bordered hoverable style={{marginTop:'10px'}} title='Proyecto #1' layout='vertical'>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
<Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
<Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
                <Descriptions.Item span={2} ><center><Button type='primary' size='small' icon={<DownloadOutlined />}>Nombre...</Button></center></Descriptions.Item>
              </Descriptions>

            </Card>
          </Col>
          <Col span={8}>
            <Card hoverable>
              <Input placeholder='Nombre ' style={{marginBottom:'10px'}} />
              <Select placeholder='Proyecto' style={{width:'100%', marginBottom:'10px'}}>
                <Select.Option>Proyecto</Select.Option>
                <Select.Option>Proyecto</Select.Option>
                <Select.Option>Proyecto</Select.Option>
                <Select.Option>Proyecto</Select.Option>
                <Select.Option>Proyecto</Select.Option>
              </Select>
              <Select placeholder='Tipo de archivo' style={{width:'100%', marginBottom:'10px'}}>
                <Select.Option>A</Select.Option>
                <Select.Option>B</Select.Option>
                <Select.Option>C</Select.Option>
                <Select.Option>D</Select.Option>
                <Select.Option>E</Select.Option>
              </Select>
              <Upload style={{marginBottom:'12px'}}>
                <Button style={{marginBottom:'12px'}}type='primary' size='small'>Adjuntar</Button>
              </Upload>

              <Button type='primary' block>Crear archivo</Button>
            </Card>
          </Col>
    </Row>)
}


export default Files 
