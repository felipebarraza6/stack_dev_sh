import React, { useState, useEffect } from 'react'
import api from '../../../api/endpoints'
import { Button, Tooltip, Descriptions } from 'antd'
import { UploadOutlined } from '@ant-design/icons'
import SingleElement from './SingleElement'

const SectionFiles = () => {

    const [elements, setElements] = useState(null)

    const getData = async() => {
        const rq = await api.projects.types_elements.list().then((r)=> {            
            setElements(r.data.results)
        })
    }

    console.log(elements)

    useEffect(()=> {
        getData()
    }, [])

    return(<>
        {elements && 
            
            elements.map((element)=> {
                return(<SingleElement element={element} />)
            })
        }
    </>)

}


export default SectionFiles