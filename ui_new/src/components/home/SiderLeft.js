import React, { useContext } from 'react'
import { Card, Button } from 'antd'
import logo from '../../assets/images/logozivo.png'
import minLogo  from '../../assets/images/min_logo.png'
import { Link, useLocation } from 'react-router-dom'
import { AppContext } from '../../App'


const SiderRight = () => {

    const location = useLocation()
    
    const { state } = useContext(AppContext)
    
    console.log(state.user.username)

    return(<Card hoverable={true} style={{backgroundColor:'#1F3461', borderRadius:'20px'}}>
    <center><img src={logo} width='50px' style={{marginBottom:'40px', }} /></center>                            
    <div style={{textAlign:'center', backgroundColor:'white', marginLeft:'-24px', marginRight:'-24px',  marginBottom:'15px',backgroundColor: location.pathname=='/'?'#1F3461':'white',}}>
        <Link to='/'><Button  type='link' style={{color:location.pathname!=='/'?'#1F3461':'white'}}>Mi Pozo</Button></Link>
    </div>
    <div style={{textAlign:'center', backgroundColor:'white', marginLeft:'-24px', marginRight:'-24px',  marginBottom:'15px',backgroundColor: location.pathname=='/graficos'?'#1F3461':'white',}}>
        <Link to='/graficos'><Button disabled={state.user.username == 'gcastro' ? true:false} type='link' style={{color:location.pathname!=='/graficos'?'#1F3461':'white'}}>Gráficos</Button></Link>
    </div>
    <div style={{textAlign:'center', backgroundColor:'white', marginLeft:'-24px', marginRight:'-24px',  marginBottom:'15px',backgroundColor: location.pathname=='/indicadores'?'#1F3461':'white',}}>
        <Link to='/indicadores'><Button disabled={state.user.username == 'gcastro' ? true:false}  type='link' style={{color:location.pathname!=='/indicadores'?'#1F3461':'white'}}>Indicadores</Button></Link>                                
    </div>
    <div style={{textAlign:'center', backgroundColor:'white', marginLeft:'-24px', marginRight:'-24px',  marginBottom:'250px',backgroundColor: location.pathname=='/reportes'?'#1F3461':'white',}}>
        <Link to='/reportes'><Button disabled={state.user.username == 'gcastro' ? true:false}  type='link' style={{color:location.pathname!=='/reportes'?'#1F3461':'white'}}>Reportes</Button></Link>                                
    </div>
    
    <div>
        <center><img src={minLogo} /></center>
    </div>
</Card>)

}


export default SiderRight
