import React, {useState} from "react"
import { Card, CardHeader, CardBody, CardTitle, Row, Col, Table } from "reactstrap"
import SortingTable from "../../components/SortingTable/SortingTable.js"

import { Input, Select, Button } from "antd"
import api_crm from '../../api_crm/endpoints' 

const RegularTables = () => {
  
  const user = JSON.parse(localStorage.getItem('user') || null)
  const selected_sensor = JSON.parse(localStorage.getItem('selected_sensor') || null)
  const persons = selected_sensor.persons
  console.log(selected_sensor.id)

  const [month, setMonth] = useState(null)

  return (
    <>
      
           
      <div className="content" style={{marginBottom: window.innerWidth > 800 ? '30px': '0px'}}>
        <Row style={{margin: window.innerWidth > 800 ?'100px':'0px', marginRight: window.innerWidth > 800 ? '200px': '0px'}}>
          <h3>DESCARGAR REPORTE POR MES</h3>
          <Col className="mb-5" md="12">
            <Select style={{width:'300px'}} placeholder="Seleccionar mes..."  onSelect={(x)=>{setMonth(x)}}>
              <Select.Option value="1">ENERO</Select.Option>
              <Select.Option value="2">FEBRERO</Select.Option>
              <Select.Option value="3">MARZO</Select.Option>
              <Select.Option value="4">ABRIL</Select.Option>
              <Select.Option value="5">MAYO</Select.Option>
              <Select.Option value="6">JUNIO</Select.Option>
              <Select.Option value="7">JULIO</Select.Option>
              <Select.Option value="8">AGOSTO</Select.Option>
              <Select.Option value="9">SEPTIEMBRE</Select.Option>
              <Select.Option value="10">OCTUBRE</Select.Option>
              <Select.Option value="11">NOVIEMBRE</Select.Option>
              <Select.Option value="12">DICIEMBRE</Select.Option>
            </Select>
            {month && 
              <Button type="primary" onClick={async()=> {
                const request = await api_crm.download_detail(selected_sensor.id, month) 
              }}>DESCARGAR</Button>
            }
          </Col>
          <Col className="mb-5" md="12">
            <Card>
              <Table responsive>
    <thead>
        <tr>
            <th className="text-center">#</th>
            <th>Nombre</th>
            <th>Email</th>
            <th className="text-center">Telefono</th>
        </tr>
    </thead>
    <tbody>
        {persons.map((x)=> <tr key={x.id}>
              <td className="text-center">{x.id}</td>
              <td>{x.name}</td>
              <td>{x.email}</td>
              <td className="text-center">{x.phone}</td>
          </tr>)}
        


    </tbody>
</Table>
          </Card>
          </Col>          
        </Row>
      </div>
    </>
  );
};

export default RegularTables;
