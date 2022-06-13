import React, { useState } from 'react'
import { Card } from 'antd'

const ModalContact = () => {

    const [visible, setVisible] = useState(true)

    return(
        <Card title='Participa' onCancel={()=>setVisible(false)} >
        </Card>
    )
}


export default ModalContact
