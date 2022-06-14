import React from "react"
import { Card, Button, CardHeader, CardBody, CardTitle, Row, Col, Table } from "reactstrap"
import SortingTable from "../../components/SortingTable/SortingTable.js"


const RegularTables = () => {
  
  const user = JSON.parse(localStorage.getItem('user') || null)
  const selected_sensor = JSON.parse(localStorage.getItem('selected_sensor') || null)
  const persons = selected_sensor.persons
  console.log(persons)

  return (
    <>
           
      <div className="content" style={{marginBottom: window.innerWidth > 800 ? '30px': '0px'}}>
        <Row style={{margin: window.innerWidth > 800 ?'100px':'0px', marginRight: window.innerWidth > 800 ? '200px': '0px'}}>
          <Col className="mb-5" md="12">
            <Card>
              <Table responsive>
    <thead>
        <tr>
            <th className="text-center">#</th>
            <th>Nombre</th>
            <th>Email</th>
            <th className="text-center">Telefono</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        {persons.map((x)=> <tr key={x.id}>
              <td className="text-center">{x.id}</td>
              <td>{x.name}</td>
              <td>{x.email}</td>
              <td className="text-center">{x.phone}</td>
              <td><Button size="sm">SOLICITAR REPORTE(en desarrollo...)</Button></td>
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
