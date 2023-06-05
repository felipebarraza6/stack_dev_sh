//React 
import React from 'react'

//Antd
import { Layout, Menu, Typography  } from 'antd'

// Antd Icons
import { DashboardOutlined,          
         UsergroupAddOutlined, 
          FolderOutlined,
         BuildOutlined, 
         ToolOutlined,
         OrderedListOutlined,
         UserOutlined,
         UnorderedListOutlined,
         ProfileFilled,
         FolderOpenOutlined, 
         BuildFilled,
         FileOutlined } from '@ant-design/icons'

//Build
import logo from '../build/images/logo-white.png'
import InternalLifting from '../components/internal_lifting/Home'

//Components
import MenuHeader from '../components/home/MenuHeader'
import Dashboard from '../components/dashboard/Dashboard'
import Enterprises from '../components/enterprises/Enterprises'
import Clients from '../components/clients/Clients'
import Tasks from '../components/tasks/Tasks'
import NotFound from '../components/errors/NotFound'
import HomeQuotation  from '../components/quotations/Home'
import Projects from '../components/projects/Projects'
import ConfigElements from '../components/config_elements/ConfigElements'
import ViewProject from '../components/projects/ViewProject'


// React Router
import { BrowserRouter, Route, Link, Switch } from 'react-router-dom'

const { Header, Content, Sider } = Layout


const Home = () =>{
        return(
          <BrowserRouter>
            <Layout style={{ minHeight: '100vh' }}>            
            <Sider style={{padding:'10px'}} width={'300px'}>
              <div>
                <Typography.Title style={{color:'white', textAlign:'left'}}>
                  ERP / <span style={{fontSize:'25px'}}>Smart Hydro</span>
                </Typography.Title>
              </div>
             <hr /> 
              <Menu theme="dark" mode="inline" style={{textAlign:'left',marginTop:'20px'}}>
                <Menu.Item key="1">
                    <Link to="/">
                    <DashboardOutlined style={{marginRight:'10px'}}/>
                     Dashboard
                     </Link>
                </Menu.Item>
                <Menu.SubMenu title={<><FolderOpenOutlined /> Clientes</>} >
                      <Menu.Item key="2">
                        <Link to="/enterprises">
                          <BuildOutlined />
                           Empresas 
                        </Link>                        
                      </Menu.Item>
                      <Menu.Item key="4">
                        <Link to="/clients">
                          <UserOutlined />
                          Personas
                        </Link>
                        
                      </Menu.Item>
                      <Menu.Item key="13">
                      <Link to="/quotations">
                          <ProfileFilled />
                           Levantamiento clientes
                        </Link>                 
                      </Menu.Item>
                      <Menu.Item key="12">
                      <Link to="/internal_lifting">
                          <ProfileFilled />
                           Levantamiento terreno
                        </Link>                 
                      </Menu.Item>
                      
                                      </Menu.SubMenu>
<Menu.SubMenu title={<><FolderOutlined />Proyectos</>} >
                      <Menu.Item key="8">
                        <Link to="/projects">
                          <FolderOpenOutlined/>
                          Gestionar proyectos
                        </Link>                        
                      </Menu.Item>                      
                      <Menu.Item key="9">
                        <Link to="/config_entry">
                          <ToolOutlined />
                          Configurar entradas
                        </Link>                        
                      </Menu.Item>
                    </Menu.SubMenu>
                  <Menu.Item key="7">
                    <Link to="/actions">
                        <UnorderedListOutlined />
                        Gestión de Tareas
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
                    <Route exact path='/quotations' component={HomeQuotation} />
                    <Route exact path='/internal_lifting' component={InternalLifting} />
                    <Route exact path='/projects' component={Projects} />
                    <Route exact path='/config_entry' component={ConfigElements} />
                    <Route exact path='/projects/:id' component={ViewProject} />
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
