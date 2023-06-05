import React, { useState, useEffect } from "react";
import { Row, Col, Upload, Typography, Tag, Form, Input, Button } from "antd";
import {
  FilePdfFilled,
  FileExcelFilled,
  FileWordFilled,
  FilePptFilled,
  FileImageFilled,
  UploadOutlined,
} from "@ant-design/icons";
import ListFilterFiles from "./ListFilterFiles";
import FormUpload from "./FormUpload";

const { Title, Paragraph } = Typography;
const { TextArea } = Input;

const UploadValueFile = ({ element }) => {
  const [properties, setProperties] = useState(null)
  const [selectFile, setSelectFile] = useState(null)
  const [count, setCount] = useState(0)

  const validateTypeFileAndColor = (type_file_str, a, color_icons, effect) => {
    let color = "";
    let str = "";
    let icon = null;
    if (type_file_str === "pdf") {
      str = ".pdf";
      color = "red";
      icon = (
        <FilePdfFilled
          style={{
            color: color_icons && color,
            fontSize: color_icons && "20px",
          }}
        />
      );
    } else if (type_file_str === "excel") {
      str = ".xls / .xlsx";
      color = "green";
      icon = (
        <FileExcelFilled
          style={{
            color: color_icons && color,
            fontSize: color_icons && "20px",
          }}
        />
      );
    } else if (type_file_str === "word") {
      str = ".doc / .docx";
      color = "blue";
      icon = (
        <FileWordFilled
          style={{
            color: color_icons && color,
            fontSize: color_icons && "20px",
          }}
        />
      );
    } else if (type_file_str === "powerpoint") {
      str = ".ppt";
      color = "orange";
      icon = (
        <FilePptFilled
          style={{
            color: color_icons && color,
            fontSize: color_icons && "20px",
          }}
        />
      );
    } else if (type_file_str === "image") {
      str = ".jpg / .png";
      color = "purple";
      icon = (
        <FileImageFilled
          style={{
            color: color_icons && color,
            fontSize: color_icons && "20px",
          }}
        />
      );
    }
    if(effect){
      setProperties({
        color: color,
        icon: icon
      })
    }
    if (a) {
      return {
        backgroundColor: color,
        borderColor: color,
      };
    } else {
      return (
        <Tag style={{ backgroundColor: color, color: "white" }}>{str}</Tag>
      );
    }
  };

  useEffect(()=> {
    validateTypeFileAndColor(element.type_file, false, true, true)
  },[])

  return (
    <Row>
      <Col span={18}>
        <Paragraph>
            Formato de archivos designados para este tipo de documento:{" "}
          {validateTypeFileAndColor(element.type_file, false, true)}
        </Paragraph>
        <ListFilterFiles properties={properties} element={element} count={count} setCount={setCount} />
      </Col>
      <Col span={6}>
        <FormUpload properties={properties} element={element} count={count} setCount={setCount} />
      </Col>
    </Row>
  );
};

export default UploadValueFile;
