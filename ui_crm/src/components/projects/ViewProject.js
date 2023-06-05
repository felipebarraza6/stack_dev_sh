import React, { useState, useEffect } from 'react'
import { Row, Col, Typography, Button, Collapse } from 'antd'
import { useLocation, Link } from "react-router-dom"
import { ArrowLeftOutlined } from '@ant-design/icons'
import api from '../../api/endpoints'
import GeneralProjectInfo from './view_projects_gadgets/GeneralProjectInfo'
import SectionFiles from './view_projects_gadgets/SectionsFiles'
const { Title, Paragraph, Text } = Typography


const ViewProject = () => {
    
    const location = useLocation()
    const [id, setId] = useState(location.pathname.slice(10))
    
    const [dataProject, setDataProject] = useState(null)

    const getData = async() => {
      const rq = await api.projects.project.retrieve(id).then((res)=> {
        console.log(res)
        setDataProject(res.data)
      })
    }

    useEffect(()=> {
      getData() 
    }, [location.pathname])

    return(<Row style={{backgroundColor: 'white', padding:'20px', borderRadius:'10px'}}>
        <Col span={18}>{dataProject && <>
            <GeneralProjectInfo project={dataProject}  />
          </>}
        </Col>
        <Col span={6} justify={'end'}>
            <Link to='/projects/'>
                <Button style={{float:'right'}} icon={<ArrowLeftOutlined />} type='primary'>Volver a todos los proyectos</Button>
            </Link>
        </Col>
        <Col span={24} style={{padding:'20px', marginTop:'20px'}}>
          <Collapse defaultActiveKey={['1']}>
            <Collapse.Panel header='Archivos' key='1'>
              <SectionFiles />
            </Collapse.Panel>
            <Collapse.Panel header='Notas' key='2'>

            </Collapse.Panel>
            <Collapse.Panel header='Levantamiento' key='3'>

            </Collapse.Panel>


          </Collapse>
        </Col>
    </Row>)

}


export default ViewProject
