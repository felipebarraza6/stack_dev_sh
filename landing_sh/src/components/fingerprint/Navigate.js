import React, { useState } from 'react'
import { Menu, Drawer } from 'antd'
import { ToolOutlined, PlusCircleOutlined, UnorderedListOutlined, CheckCircleTwoTone, CloseCircleOutlined } from '@ant-design/icons'
import DrawerSupport from './DrawerSupport'
import glosary from '../../assets/files/glosario.pdf'
import accession from '../../assets/files/formulario-de-adhesion.docx'

const Navigate = ({ elements, state, setState }) => {
  
  const [stateNavigate, setStateNavigate] = useState({
    drawerSupportOpen: false,
    drawerIsCreate:false,
    tickets: null
  })

  return(<>
    <DrawerSupport is_open={stateNavigate.drawerSupportOpen} 
      is_create={stateNavigate.drawerIsCreate}
      setStateNavigate={setStateNavigate}
      tickets={stateNavigate.tickets} />
    <Menu mode='inline'>{elements && <>
        <Menu.Item onClick={()=> window.open(glosary)}>
      GLOSARIO
    </Menu.Item>
    <Menu.Item onClick={()=> window.open(accession)}>
      ANEXO FORMULARIO DE ADHESIÓN
    </Menu.Item>
    {elements.map((module) => <Menu.SubMenu title={`Etapa ${module.id} :${module.name}`}>
      {module.sections.map((section) => <Menu.Item onClick={(e) => setState({ ...state, section_selected: section})}>
        {section.is_validated ? <CheckCircleTwoTone />:<CloseCircleOutlined />} {module.id}.{section.id}) {section.name}
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
    </Menu.SubMenu>)}    
    </>}
  </Menu></>)

}


export default Navigate
