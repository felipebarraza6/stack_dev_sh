import React, { 
    createContext, 
    useContext } from 'react'
import { Row, Col } from 'antd'
import AddWell from './AddWell'
import WellData from './WellData'
import { QuotationContext } from '../../../containers/Quotation'

export const WellContext = createContext()

const Well = () => {

    const { state, 
            dispatch } = useContext(QuotationContext)

    const createOrEdit = state.wells.temporary_well.create_or_edit

    return(<Row align={'center'}>
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