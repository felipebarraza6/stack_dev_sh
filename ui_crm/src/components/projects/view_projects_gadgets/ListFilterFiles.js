import React, { useState, useEffect } from "react";
import { Card, Row, Col, Popconfirm, Button, Typography, Tag, notification } from "antd";
import { SearchOutlined, FileImageFilled } from "@ant-design/icons";
import api from "../../../api/endpoints";
import { useLocation } from "react-router-dom"
import UploadFile from "./UpdateFile";

const { Paragraph } = Typography;

const ListFilterFiles = ({ properties, element, count, setCount }) => {
  console.log(element)
  const location = useLocation()
  const [files, setFiles] = useState([])
  console.log(files)

  const getData = async() => {
    const rq = await api.projects.values_elements.list(location.pathname.slice(10), element.id).then((r)=> {
      setFiles(r.data.results)
    })
  }

  const formatDate = (x) => {
    var date = new Date(x)
    const opciones_dia = { day: 'numeric', weekday: 'long' };

    var str_day = date.toLocaleDateString('es-ES', opciones_dia);
    //Freitag, 2. Juli 2021
    var return_str = `${str_day.slice(0,3).toUpperCase()} ${date.getDate()}-${date.getMonth()+1>9?`${date.getMonth()+1}`:`0${date.getMonth()+1}`}-${date.getFullYear()}`
   return return_str
  }

  useEffect(()=> {
    getData()
    formatDate(element.created)
  }, [count])

  return (
    <Row style={{ marginRight: "10px" }}>      
      <Col span={24}>
        <Row style={{ marginTop: "10px" }}>
          {files.map((file)=> {
            return(<Col span={8}>
              <Card
                hoverable
                bordered
                title={
                  <>
                  {properties && properties.icon} {file.name.toUpperCase()}
                  </>
                }
                extra={file.code}
                style={{borderColor:properties&&properties.color, borderRadius:'10px', borderWidth:'2px'}}
              >
                <Tag color={properties&&properties.color}>{formatDate(file.created.slice(0,10))} /{file.created.slice(11,16)}hrs</Tag>
  
                
                <Paragraph style={{ marginTop: "20px" }}>
                {file.note !== 'undefined' ?
                  <>{file.note}</>:''}
                </Paragraph>
                <Row justify="center">
                  <Col span={24}>                    
                    <UploadFile properties={properties&&properties} file={file} count={count} setCount={setCount} />
                    <Button onClick={()=>window.open(file.file)} type="primary" size="small" style={{ margin: "5px", backgroundColor: properties&&properties.color, borderColor: properties&&properties.color}}>
                      Descargar
                    </Button>
                    <Popconfirm title='Estas seguro de eliminar este archivo?' onConfirm={async()=> {
                      const rq = await api.projects.values_elements.delete(file.id).then((r)=>{
                        notification.error({message:'Archivo eliminado correctamente'})
                        setCount(count+1)
                      })
                    }}  >
                      <Button
                        type="primary"
                        size="small"
                        style={{ margin: "5px" }}
                        danger>
                        Eliminar
                      </Button>
                    </Popconfirm>
                  </Col>
                </Row>
              </Card>
            </Col>)
          })}
          
        </Row>
      </Col>
    </Row>
  );
};

export default ListFilterFiles;
