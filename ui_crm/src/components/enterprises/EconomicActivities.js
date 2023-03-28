import React, { useState, useEffect } from 'react'
import api from '../../api/endpoints'
import { Select } from 'antd'

const EconomicActivities = () => {

  const [list, setList] = useState([])

  const getData = async() => {
    const rq = await api.enterprises.list_economic().then((res)=> {
      setList(res.data.results)
    }) 
  }

  useEffect(()=> {
    getData()
  }, [])
  
  return(<Select placeholder='selecciona una opción'>
      {list.map((x)=><Select.Option value={x.value}>{x.name}</Select.Option>)}
    </Select>)

}


export default EconomicActivities
