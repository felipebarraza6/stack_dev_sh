import React from 'react'
import { Menu } from 'antd'
import { AppstoreOutlined, MailOutlined, SettingOutlined } from '@ant-design/icons';


const Navigate = () => {
  
  function getItem(label, key, icon, children, type) {
  return {
    key,
    icon,
    children,
    label,
    type,
  };
  }

  const items = [
  getItem('Navigation One', 'sub1', <MailOutlined />, [
    getItem('Item 1', 'g1', null, [getItem('Option 1', '1'), getItem('Option 2', '2')], 'group'),
    getItem('Item 2', 'g2', null, [getItem('Option 3', '3'), getItem('Option 4', '4')], 'group'),
  ]),
  getItem('Navigation Two', 'sub2', <AppstoreOutlined />, [
    getItem('Option 5', '5'),
    getItem('Option 6', '6'),
    getItem('Submenu', 'sub3', null, [getItem('Option 7', '7'), getItem('Option 8', '8')]),
  ]),
  getItem('Navigation Three', 'sub4', <SettingOutlined />, [
    getItem('Option 9', '9'),
    getItem('Option 10', '10'),
    getItem('Option 11', '11'),
    getItem('Option 12', '12'),
  ]),
]

  return(<><Menu mode='inline'>
      <Menu.SubMenu title='Etapa 1: Administrativa'>
        <Menu.Item>
          Actividad 1.1
        </Menu.Item>
        <Menu.Item>
          Actividad 1.2
        </Menu.Item>
        <Menu.Item>
          Actividad 1.3
        </Menu.Item>
        <Menu.Item>
          Actividad 1.4
        </Menu.Item>
      </Menu.SubMenu>
    <Menu.SubMenu title='Etapa 2: Legal'>
        <Menu.Item>
          Actividad 2.1
        </Menu.Item>
        <Menu.Item>
          Actividad 2.2
        </Menu.Item>
        <Menu.Item>
          Actividad 2.3
        </Menu.Item>
        <Menu.Item>
          Actividad 2.4
        </Menu.Item>
      </Menu.SubMenu>
    <Menu.SubMenu title='Etapa 3: Tecnica'>
        <Menu.Item>
          Actividad 3.1
        </Menu.Item>
        <Menu.Item>
          Actividad 3.2
        </Menu.Item>
        <Menu.Item>
          Actividad 3.3
        </Menu.Item>
        <Menu.Item>
          Actividad 3.4
        </Menu.Item>
      </Menu.SubMenu>
    </Menu>
    </>)

}


export default Navigate
