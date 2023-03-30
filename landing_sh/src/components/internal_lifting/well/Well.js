import React, { 
    createContext, 
    useContext } from 'react'
import { Row, Col } from 'antd'
import AddWell from './AddWell'
import WellData from './WellData'
import { QuotationContext } from '../../../containers/Quotation'
import { InternalLiftingContext } from '../../pages/InternalLifting'

export const WellContext = createContext()

const Well = () => {

    const { state, 
            dispatch } = useContext(InternalLiftingContext)

    const createOrEdit = state.wells.temporary_well.create_or_edit

    return(<Row align={'center'} style={{marginTop: window.innerWidth>900&&'0px'}}>
        <Col span={!createOrEdit ? 24: window.innerWidth > 800 ? 12:24} style={styles.container}>
            {createOrEdit ? 
            <AddWell />:<WellData />}
        </Col>
    </Row>)

}

const styles = {
    container:{
        paddingLeft:'2%',
        paddingRight: '2%',
        paddingBottom:'20%',
        paddingTop:'0%'
    },        
}


export default Well