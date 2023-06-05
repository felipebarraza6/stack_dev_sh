import React,{useReducer, useEffect} from 'react'

import {Row, Col, Card, Pagination, Spin, Skeleton } from 'antd'

//Reducer
import { reducer } from '../../reducers/clients.js'

//Components
import Totals from './Totals'
import CardEnterprise from './CardEnterprise'
import TableClients from './TableClients'
import ModalFrom from './ModalForm'
import ModalUpdateForm from './ModalUpdateForm'

//Actions
import { getEnterprises } from '../../actions/employess'
import { getTotals } from '../../actions/employess'
import { getPersons,createPerson, updatePerson } from '../../actions/employess'


const Clients = () =>{

    const initialState = {
        loading:false,
        loading_cards:false,
        loading_table: false,

        enterprises:null,
        pageEnterprise:1,
        
        dataClients:null,
        currentPage: 1,
        enterprise_selected:'',
        quantity_persons:null,
        pageTable:1,

        enterpriseModal:null,
        modalFormVisible: false,

        modalUpdateVisible: false,
        personModal: null,
                
        totals:null,        

        error:null
    }  

    const [state, dispatch] = useReducer(reducer, initialState)
    
    const elementsSkeleton = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] 
    
    useEffect(() => {
        
        dispatch({type:'LOADING'})
        
        getTotals(dispatch)

        getEnterprises(dispatch, 1)

        getPersons(dispatch, 1, '')
       
    }, [])
    
    

    return(
        <>     
        
        {state.modalFormVisible &&
        <ModalFrom visible={state.modalFormVisible} onCreate={(values) => createPerson(dispatch,values, state.enterpriseModal, state.pageTable)} enterprise={state.enterpriseModal} onCancel={ () => dispatch({type:'OFF_MODAL_CREATE' })} error={state.error}/>
        }

        {state.modalUpdateVisible &&
        <ModalUpdateForm visible={state.modalUpdateVisible} onCreate={(values) => updatePerson(dispatch, values, state.pageTable, state.enterprise_selected, values)} person={state.personModal} onCancel={()=> 
        
        dispatch({type:'OFF_MODAL_UPDATE'}) }/>}
        
        {state.loading ? <Spin size="large" style={{ marginLeft:'40%', marginTop:'15%'}} />:
        <>
        <Row style={{marginBottom:'20px'}}>
            {state.totals && <Totals data={state.totals} />}            
        </Row>
        <Row style={{marginBottom:'20px'}}>
        <Col span={16}>                    
            
            {state.loading_cards ?                  
                <>
                <Row>
                    {elementsSkeleton.map((number) => 
                        <Card.Grid key={number} hoverable={false} style={{backgroundColor:'white', width:'282px'}}>
                            <Skeleton active />
                        </Card.Grid>
                    )}                                   
                </Row>
                
                </>
                :
                <Row>
                    {state.enterprises && state.enterprises.results.map((value) =>
                        <Card.Grid key={value.id} style={{backgroundColor:'white', width:'282px'}}>
                        <CardEnterprise 
                            data={value} 
                            dispatch={dispatch} 
                            employess={state.personsEnterprise}
                            loading={state.loading_cards}                                                         
                        />
                    </Card.Grid>
                    )}                    
                </Row>
                }        
                <Row style={{margin:'20px'}}>
                { state.enterprises && <Pagination size="small" total={state.enterprises.count} onChange={(page)=> getEnterprises(dispatch, page)} />}
                </Row>                                
            </Col>            
            <Col style={{paddingRight:'20px'}} span={8}>
                <TableClients 
                    dispatch={dispatch} 
                    data={state.dataClients} 
                    loading={state.loading_table}
                    quantity={state.quantity_persons}
                    enterprise={state.enterprise_selected}
                    page={state.pageTable} 
                />
            </Col>
        </Row>
        </>
        }
        </>
    )
}

export default Clients
