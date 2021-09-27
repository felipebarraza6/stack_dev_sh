//React
import React, { useContext }  from 'react' 

//Ant Design
import { Menu } from 'antd'
import { LogoutOutlined } from '@ant-design/icons'
 
//Auth Context
import { AuthContext } from '../../App'

//Components Child in Home
import Profile from './Profile'


const MenuHeader = () =>{   

    const rightStyle = {position: 'absolute', top: 0, right: 0}    

    const { dispatch } = useContext(AuthContext)

    const Logout = () => dispatch({
            type: 'LOGOUT'
    })

    return (                
            <Menu mode="horizontal" theme="dark" style={rightStyle}>
                <Profile />
                <Menu.Item onClick={Logout}>
                    <LogoutOutlined />
                    Cerrar Sesión
                </Menu.Item>
            </Menu>                
    )

}

export default MenuHeader