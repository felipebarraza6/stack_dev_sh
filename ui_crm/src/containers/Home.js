//React 
import React from 'react'

//Antd
import { Layout, Menu  } from 'antd'

// Antd Icons
import { DashboardOutlined,          
         UsergroupAddOutlined, 
         BuildOutlined, 
         UnorderedListOutlined} from '@ant-design/icons'

//Build
import logo from '../build/images/logo-white.png'

//Components
import MenuHeader from '../components/home/MenuHeader'
import Dashboard from '../components/dashboard/Dashboard'
import Enterprises from '../components/enterprises/Enterprises'
import Clients from '../components/clients/Clients'
import Tasks from '../components/tasks/Tasks'
import NotFound from '../components/errors/NotFound'

// React Router
import { BrowserRouter, Route, Link, Switch } from 'react-router-dom'

const { Header, Content, Sider } = Layout


const Home = () =>{
        return(
          <BrowserRouter>
            <Layout style={{ minHeight: '100vh' }}>            
            <Sider style={{padding:'20px'}}>
              <div style={{alignItems:'center'}}>
                  <img alt='logo' style={{width:'80%', marginRight:'50px', marginTop:'40px', marginBottom:'40px'}} src={logo} />
              </div>
              
              <Menu theme="dark" mode="inline">
                <Menu.Item key="1">
                    <Link to="/">
                    <DashboardOutlined style={{marginRight:'10px'}}/>
                     Dashboard
                     </Link>
                </Menu.Item>
                  <Menu.Item key="2">
                    <Link to="/enterprises">
                        <BuildOutlined/>
                        Empresas
                      </Link>
                    </Menu.Item>
                    <Menu.Item key="3">
                    <Link to="/clients">
                        <UsergroupAddOutlined />
                        Clientes
                      </Link>
                    </Menu.Item>
                    <Menu.Item key="4">
                    <Link to="/actions">
                        <UnorderedListOutlined />
                        Tareas
                      </Link>
                    </Menu.Item>                
              </Menu>
              
            </Sider>

            <Layout>              
            <Header >
                <MenuHeader />                                        
            </Header>
              <Content>
                
                <div style={{ padding: 24, minHeight: 360, textAlign:'left' }}>
                  <Switch>                
                    <Route exact path='/' component={Dashboard} />
                    <Route exact path='/enterprises' component={Enterprises} />
                    <Route exact path='/clients' component={Clients} />
                    <Route exact path='/actions' component={Tasks} />
                    <Route path="*" component={NotFound} />
                 </Switch>
                </div>
                
              </Content>              
            </Layout>

          </Layout>
          </BrowserRouter>

                            
        )
    }


export default Home