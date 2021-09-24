import React, {useReducer, useEffect} from 'react'

import { Row, Col, Spin } from 'antd'

//Reducer
import { reducer } from '../../reducers/enterprises'

//Actions
import { getTotals, getPagination } from '../../actions/enterprises'

//Components
import Totals from './Totals'
import FormSteps from './FormSteps'
import ListEnterprise from './ListEnterprise'
import EnterpriseForm from './EnterpriseForm'

const Enterprises = () =>{

    const initialState = {
        loading: false,
        totals: {
            enterprises: 0,
            enterprises_actives: 0,
            enterprises_inactive: 0        
        },               

        enterprise: null,
        loading_content: null,

        loading_form: null,        

        page:1,
        quantity: null,
        loading_table: false,

        error: null
    }

    useEffect(() => {
       
        getTotals(dispatch)

    }, [])

    const [state, dispatch] = useReducer(reducer, initialState)
    

    return(
            <>            
                {state.loading ? <Spin size="large" style={{ marginLeft:'40%', marginTop:'15%'}} />:
                <React.Fragment>                    
                    <Row style={{marginBottom:'20px'}}>

                        <Totals data={state.totals} />
                        
                    </Row>
                    <Row style={{marginLeft:'0px', marginRight: '30px'}}>
                        
                        <Col style={{paddingRight:'20px'}} span={12}>                            
                            <FormSteps enterprise = {state.enterprise} dispatch={dispatch} loading = {state.loading_content} />                           
                            <EnterpriseForm dispatch = {dispatch} state= {state} />
                        </Col>
                        
                        <Col style={{paddingLeft:'20px'}} span={12} >                                           
                            
                            <ListEnterprise 
                                data={state.data} 
                                loading = {state.loading_table} 
                                page = {state.page} 
                                quantity = {state.quantity}
                                pagination = {getPagination}                                                            
                                dispatch = {dispatch}
                            />

                        </Col>

                    </Row>
                </React.Fragment>
                }
            </>        
    )
}

export default Enterprises