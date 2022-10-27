import React, { useContext } from 'react'
import { QuotationContext } from '../../containers/QuotationExternalClients'
import { Steps } from 'antd'
import { ProfileOutlined, AppstoreOutlined, 
        FileImageOutlined, EyeOutlined } from '@ant-design/icons'

const Header = () => {
  const { state }  = useContext(QuotationContext)
  const steps = state.steps

  return(<>
    <Steps size='default' style={styles.container} 
       current = {steps.current} >
      {!steps.step01.hide && 
        <Steps.Step icon={<ProfileOutlined />}  title={steps.step01.finish ? state.client.name_enterprise : steps.step01.title} />}
      {!steps.step02.hide && 
        <Steps.Step icon={<AppstoreOutlined />} title={steps.step02.title} />}
      {!steps.step03.hide && 
        <Steps.Step icon={<FileImageOutlined />} title={steps.step03.title} />}
      {!steps.step04.hide && 
        <Steps.Step icon={<EyeOutlined />} title={steps.step04.title} />}
    </Steps>
  </>)

}


const styles = {
  container: {
    padding: '20px',
    backgroundColor: 'white'
  }
}

export default Header
