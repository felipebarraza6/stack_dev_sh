import React from 'react'

import { Collapse, Select } from 'antd'
import { BuildTwoTone } from '@ant-design/icons'

import {searchEnterprise} from '../../actions/enterprises'
import {reloadTasks} from '../../actions/tasks'

const { Panel } = Collapse
const { Option } = Select


const FilterEnterprise = (attr) =>{
    
    const options = attr.state.filter_enterperises

    const dispatch = attr.dispatch

    return(
        <Collapse>
             <Panel header={<>Empresa<BuildTwoTone style={{float: 'right'}} /></>}>
                <Select
                    showSearch
                    placeholder="Buscar Empresa"
                    optionFilterProp="children"
                    notFoundContent={'No se encuentra'}

                    onSearch={(value)=>{

                        searchEnterprise(attr.dispatch, value)
                    }}                    

                    onSelect={(value) => {
                        
                        dispatch({type: 'CLEAN_IDS_SELECTED'})
                        
                        dispatch({type: 'ENTERPRISE_SELECTED', value:value})

                        reloadTasks(
                            attr.dispatch, 
                            {
                                totals:1, 
                                actives:1, 
                                priorities:1, 
                                completes:1
                            }, 
                            {
                                start_date:attr.state.date_range.start_date, 
                                end_date:attr.state.date_range.end_date
                            },
                            attr.state.year,
                            attr.state.month,
                            attr.state.day,
                            '',
                            value
                            

                        )
                    }}
                    
                    style={{width:'100%'}}
                >
                    {options &&
                    options.map((option)=> (
                    <Option key={option.id} value={option.id}>{option.name}</Option>
                    )

                    )}
                </Select>                 
             </Panel>
        </Collapse>
    )
}

export default FilterEnterprise