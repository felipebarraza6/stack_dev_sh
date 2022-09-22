import React, { useState, useEffect } from 'react'
import  api from '../../api/endpoints'
import { Table, Button } from 'antd'

const Home = () => {

    const [listQuotations, setListQuotations] = useState([])
    
    async function getData(){
      const rq = await api.quotation.list().then((x)=> {
        console.log(x)
        setListQuotations(x.data.results)
      })
      return rq
    }

    console.log(listQuotations)

    useEffect(() => {
      getData()
    }, [])

    return(<Table
        columns = {[
          {
            title:'URL Cotización',
            render: (x)=> <>
              <a href={`https://smarthydro.cl/dgaform/external_client/${x.uuid}`} target="_blank">{x.uuid}</a>
            </>
          }, 
          {
            render: (x)=> <>
              <Button>Ver datos</Button>
            </>
          },
          {
            title: 'Está aprobada?',
            render: (x)=> {
              if(x.is_approved){
                return(<Button type='primary' danger>CANCELAR APROBACIÓN</Button>)
              } else {
                return(<Button type='primary'>APROBAR</Button>)
              }
            }
          }
        ]}
        dataSource={listQuotations}></Table>)
}


export default Home
