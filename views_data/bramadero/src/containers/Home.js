//React 
import React from 'react'

//Antd
import { Layout  } from 'antd'

//Build
import logo from '../build/images/logo-white.png'

//Components
import MenuHeader from '../components/home/MenuHeader'
import Dashboard from '../components/dashboard/Dashboard'
import NotFound from '../components/errors/NotFound'

// React Router
import { BrowserRouter, Route, Switch } from 'react-router-dom'
const { Header, Content } = Layout


const Home = () =>{
        
        return(
          <BrowserRouter>
            <Layout style={{ minHeight: '100vh' }}>            
            <Header >
                <img width={'100px'}  src = {logo} />
                <MenuHeader />                                        
            </Header>
              <Content>
                
                <div style={{ textAlign:'center', overflow:'true' }}>
                  <Switch>                
                    <Route exact path='/' component={Dashboard} />
                    <Route path="*" component={NotFound} />
                 </Switch>
                </div>
                
              </Content>              

          </Layout>
          </BrowserRouter>
        )
    }


export default Home
