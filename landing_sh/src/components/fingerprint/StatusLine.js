import React from 'react'
import { LoadingOutlined, 
        ClockCircleOutlined,
        SmileOutlined, 
        SolutionOutlined, 
        UserOutlined, CheckCircleOutlined } from '@ant-design/icons'
import { Steps } from 'antd'
const { Step } = Steps


const StatusLine = ({ section }) => {
  var joined = 'wait'
  var in_validate = 'wait'
  var is_complete = 'wait'

  if(section && section.joined){
    joined='complete'
    in_validate='complete'
  } 
  if(section && section.is_complete){
    is_complete='complete'
  }
  

return(<Steps>
    {section ? <>
        <Step status={joined} title="Ingreso" icon={<UserOutlined />} />
        <Step status={in_validate} title={section.in_validate ? "En validacion" : "Validado"} icon={in_validate == 'complete' ? <>
      {section.in_validate ? <LoadingOutlined /> : <SolutionOutlined />}          
        </>:<ClockCircleOutlined />} />
        <Step status={is_complete} title="Completado" icon={<CheckCircleOutlined style={{color:'green'}} />} />    
      </>:<>
        <Step status="wait" title="Ingreso" icon={<UserOutlined />} />      
        <Step status="wait" title="En validacion" icon={<ClockCircleOutlined />} />
        <Step status="wait" title="Completado" icon={<SmileOutlined />} />
    </>}
  </Steps>)

}


export default StatusLine
