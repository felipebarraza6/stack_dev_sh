import React, { useState, useEffect } from 'react'
import { Menu, Spin, Button, Modal } from 'antd'
import { ToolOutlined, PlusCircleOutlined, 
        UnorderedListOutlined, CheckCircleTwoTone, 
        CloseCircleOutlined, BookOutlined, CheckCircleOutlined} from '@ant-design/icons'
import DrawerSupport from './DrawerSupport'
import glosary from '../../assets/files/glosario.pdf'

const Navigate = ({ elements, state, setState }) => {

  const [isComplete, setIsComplete] = useState(false)
  
  const [stateNavigate, setStateNavigate] = useState({
    drawerSupportOpen: false,
    drawerIsCreate:false,
    tickets: null
  })

  useEffect(() => {
    if(elements){
      if(elements[0].is_complete && elements[1].is_complete){
          setIsComplete(true)
      }
    }
  }, [])


  return(<>
        <Menu mode='inline' style={{border:'2px solid #002766', borderRadius:'10px 10px 0px 0px'}}>{elements && <>
        <Menu.Item onClick={()=> window.open(glosary)} icon={<BookOutlined />}>
          GLOSARIO
        </Menu.Item>
    {elements.map((module) => <>{!module.is_hidden && <Menu.SubMenu disabled={module.is_blocked} title={`Etapa ${module.id} :${module.name}`} icon={module.is_complete ? <CheckCircleOutlined style={{color:'green'}}/>:<CloseCircleOutlined style={{color:'red'}} />}>
      {module.sections.map((section) => <Menu.Item onClick={(e) => setState({ ...state, section_selected: section})}>
        {section.is_complete ? <>
          <CheckCircleOutlined style={{color:'green'}} />
          </>:<>
            {section.in_validate ? <Spin />:
              <CloseCircleOutlined style={{color:'red'}} />}
          </>
        } {module.id}.{section.id}) {section.name}
      </Menu.Item>)}
      <Menu.SubMenu title='SOPORTE' icon={<ToolOutlined />}>
        <Menu.Item icon={<PlusCircleOutlined />} onClick={() => setStateNavigate({...stateNavigate, drawerSupportOpen:true, drawerIsCreate: true}) }>
          ABRIR TICKET
        </Menu.Item>
        <Menu.Item icon={<UnorderedListOutlined />} 
          onClick={()=> 
            setStateNavigate({
              ...stateNavigate, 
              drawerSupportOpen:true, 
              drawerIsCreate:false,
              tickets: module.tickets
            })
          }>
          TICKETS 
        </Menu.Item>
      </Menu.SubMenu>
    </Menu.SubMenu>}</>
    
  )}    
      {isComplete && <Button type='primary' style={{
          marginTop:'10px', 
          marginLeft:'20px', 
          marginBottom:'20px'}} onClick={()=> Modal.success({title:'DATOS ENVIADOS CORRECTAMENTE, NUESTRO EQUIPO TE CONTACTARA EN LAS PROXIMAS HORAS...', content:<center><Spin style={{ marginBottom:'10px', marginTop:'10px', paddingLeft:'30px'}} size='large' /></center>, width:'500px'})}>ENVIAR A ADMISIBILIDAD(Etapa 1 y 2)</Button>}
    </>}
  </Menu>
    </>)

}


const styles = {
  BookOutlined: {
    marginRight: '20px'
  }
}


export default Navigate
