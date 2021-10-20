import React, { useState, useEffect} from 'react'
import { Steps, Row, Typography } from 'antd'
import Polykarpo from './Polykarpo'


let { Step  } = Steps


const Dashboard = () =>{
    const [current, setCurrent] = useState(0)
      
       return(
            <>
             <Row>              
            </Row>       
            <Row align='center'>
              
                <Polykarpo />                  
              
            </Row>
            
            
            </>
        
        )
}

export default Dashboard
