import React, { useContext } from 'react'
import { AppContext } from '../../App'
import { Typography, Card } from 'antd'
import { useLocation } from 'react-router-dom'

const { Title } = Typography

const SiderLeft = () => {

    const { state } = useContext(AppContext)
    let location = useLocation()
    console.log(state)
  console.log(location.pathname)
    

    return(<Card hoverable={true} style={{backgroundColor:'#1F3461', borderRadius:'20px',paddingRight:'5px', paddingLeft:'5px'}}>
      {location.pathname === '/graficos' ? <>
          
          {state.list_default.map((x)=><div>
            {state.type_graph === 'm3' && 
              <p style={{color:'white', marginBottom:'5px', textAlign:'center'}}>{x.date.slice(0,2)}:00 - {x['m3/hora']} m³/h</p>
            }
            {state.type_graph === 'm3m' && 
              <p style={{color:'white', marginBottom:'5px', textAlign:'center'}}>{x.date}: {x['m3/dia']} m³/d</p>
            }
             {state.type_graph === 'niv' && 
              <p style={{color:'white', marginBottom:'5px', textAlign:'center'}}>{x.date}: {x['m/dia']} m/d</p>
            }

            </div>)}


        </>:<>
        <Title align='center' style={{color:'white'}} level={3}> {state.selected_profile.title} </Title>
    <Title align='center' style={{color:'white', marginTop:'-10px'}} level={5}> {state.user.first_name.toUpperCase()} </Title>
    <div style={{textAlign:'center', backgroundColor:'white', marginLeft:'-24px', marginRight:'-24px', marginBottom:'30px'}}>
        Profundida del pozo:<br/>
        <b><Typography.Paragraph style={{fontSize:'16px'}}> {parseFloat(state.selected_profile.d1).toFixed(0)} mtrs</Typography.Paragraph></b>
    </div>
    <div style={{textAlign:'center', backgroundColor:'white', marginLeft:'-24px', marginRight:'-24px', marginBottom:'30px'}}>
        Posicionamiento de bomba:<br/>
        <b><Typography.Paragraph style={{fontSize:'16px'}}> {parseFloat(state.selected_profile.d2).toFixed(0)} mtrs</Typography.Paragraph></b>
    </div>
    <div style={{textAlign:'center', backgroundColor:'white', marginLeft:'-24px', marginRight:'-24px', marginBottom:'30px'}}>
        Posicionamiento de sensor (freatico):<br/>
        <b><Typography.Paragraph style={{fontSize:'16px'}}>{parseFloat(state.selected_profile.d3).toFixed(0)} mtrs</Typography.Paragraph></b>
    </div>
    <div style={{textAlign:'center', backgroundColor:'white', marginLeft:'-24px', marginRight:'-24px', marginBottom:'30px'}}>
        Diámetro ducto de salida (bomba)<br/>
        <b><Typography.Paragraph style={{fontSize:'16px'}}>{parseFloat(state.selected_profile.d4).toFixed(0)} pulg</Typography.Paragraph></b>
    </div>
    <div style={{textAlign:'center', backgroundColor:'white', marginLeft:'-24px', marginRight:'-24px', marginBottom:'50px'}}>
        Diámetro flujometro<br/>
        <b><Typography.Paragraph style={{fontSize:'16px'}}>{parseFloat(state.selected_profile.d5).toFixed(0)} pulg</Typography.Paragraph></b>
    </div>

        </>}
    </Card>)

}


export default SiderLeft
