import React from 'react'

import { Result, Button } from 'antd'
import { Link } from 'react-router-dom'

const NotFound = () =>{
    return(
    <Result
        status="404"
        title="404"
        subTitle="Sorry! peeero está página no existe!"
        extra={<><Button type="primary"><Link to='/' type='primary'>Volver al Dashboard</Link></Button></>}
    >

    </Result>
    )
}

export default NotFound