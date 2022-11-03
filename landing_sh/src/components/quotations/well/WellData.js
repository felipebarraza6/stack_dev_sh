import React, { useContext } from 'react'
import { Row, Col } from 'antd'
import GeneralWell from './GeneraWell'
import { QuotationContext } from '../../../containers/Quotation'
import ListFormDataWell from './ListFormDataWell'
import WellDisplay from './WellDisplay'

const WellData = () => {

    const { state, dispatch } = useContext(QuotationContext)

    return(<Row>
        <Col span={window.innerWidth > 800 ? 5:24} style={styles.col}>            
            <GeneralWell />            
        </Col>
        <Col span={window.innerWidth > 800 ? 9:24} style={styles.col}>
            <ListFormDataWell />
        </Col>
        {window.innerWidth > 800 && <Col span={10} style={styles.col}>
            <WellDisplay />
        </Col>}
    </Row>)
}


const styles = {
    col: {
        paddingRight: '10px',
        padding: window.innerWidth > 800 ? '0px':'5px'
    }
}

export default WellData