import React, { useState, useEffect } from 'react'
import { Table, Button, Popconfirm, notification} from 'antd'
import api from '../../api/endpoints'

const ListElements = ({count, setCount, setSelectElement}) => {

    const [elements, setElements] = useState([])

    const columns = [
        { title:'Nombre', dataIndex: 'name'},
        { title:'Descripción', dataIndex: 'description'},
        { title:'Posicion', dataIndex: 'position'},
        { title:'Formato', render: (x)=> x.type_file ? x.type_file:'NO ES ARCHIVO'},
        {render: (x)=>{
            return(<>
                <Button style={{marginRight:'10px'}} size='small' type='primary' onClick={()=>setSelectElement(x)}>Editar</Button>
                <Popconfirm title='Estas seguro de eliminar esta entrada?' onConfirm={async()=> {
                    const rq = await api.projects.types_elements.delete(x.id).then((r)=> {
                        setCount(count+1)
                        notification.success({message:'Entrada eliminada!'})
                    })
                }}>
                    <Button type='primary' danger size='small'>Eliminar</Button>
                </Popconfirm>
            </>)
        }}
    ]

    const getData = async() => {
        const rq1 = await api.projects.types_elements.list().then((r)=> {
            setElements(r.data.results)
        })
    }

    useEffect(()=> {
        getData()
    }, [count])

    return(<Table size='small' dataSource={elements} style={{padding:'0px'}} bordered columns={columns} />)
}


export default ListElements
