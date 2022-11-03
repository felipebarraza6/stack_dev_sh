import React,{ useContext } from 'react'
import { QuotationContext } from '../../../containers/Quotation'
import { Descriptions, Button, Card,
        Row, Col, Typography } from 'antd'

import { EditOutlined } from '@ant-design/icons'        

const { Item } = Descriptions
const { Paragraph } = Typography

const GeneralWell = () => {

    const { state, dispatch } = useContext(QuotationContext)

    const changeCreateOrEdit = () => {
        dispatch({
            type: 'CHANGE_CREATE_OR_EDIT',
            option: true            
        })
    }

    return(<Card title='Datos generales'>
            {state.wells.temporary_well.general_data && 
            <Row justify='center' >
                <Col span='24'>                    
                    <Paragraph>{state.wells.temporary_well.general_data.name_well.toUpperCase()}</Paragraph>
                    <Paragraph >{state.wells.temporary_well.general_data.type_captation.toUpperCase()}</Paragraph>
                    <Paragraph>{state.wells.temporary_well.general_data.address_exact}</Paragraph>
                    <Button style={styles.itemBtn} type='primary' icon={<EditOutlined />}
                        size='small' onClick={changeCreateOrEdit}>Editar datos generales</Button>            
                </Col>
            </Row>}
        </Card>)
}


const styles = {
    itemBtn: {
        marginTop:'-10px',        
    }
}


export default GeneralWell

