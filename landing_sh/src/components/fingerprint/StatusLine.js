import React from 'react'
import { LoadingOutlined, 
        SmileOutlined, 
        SolutionOutlined, 
        UserOutlined } from '@ant-design/icons'
import { Steps } from 'antd'
const { Step } = Steps


const StatusLine = () => {

return(<Steps>
    <Step status="finish" title="Ingreso" icon={<UserOutlined />} />
    <Step status="finish" title="Verificacion" icon={<SolutionOutlined />} />
    <Step status="process" title="En validacion" icon={<LoadingOutlined />} />
    <Step status="wait" title="Completado" icon={<SmileOutlined />} />
  </Steps>)

}


export default StatusLine
