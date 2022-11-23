import React, { useContext } from 'react'
import { AppContext } from '../../App'
import { Typography, Card } from 'antd'

const { Title } = Typography

const SiderLeft = () => {

    const { state } = useContext(AppContext)
    

    return(<Card hoverable={true} style={{backgroundColor:'#1F3461', borderRadius:'20px',paddingRight:'5px', paddingLeft:'5px'}}>
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
</Card>)

}


export default SiderLeft