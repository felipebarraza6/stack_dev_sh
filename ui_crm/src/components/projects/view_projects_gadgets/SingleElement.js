import React, { useEffect, useState } from "react";
import { Tooltip, Button, Modal } from "antd";
import { FilePdfFilled, FileWordFilled, FileExcelFilled, FilePptFilled, FileImageFilled } from "@ant-design/icons";
import UploadValueFile from "./UploadValueFile";

const SingleElement = ({ element }) => {

  const [open, setOpen] = useState(false)
  
  const toggleModal = () => {
    if(open){
      setOpen(false)
    } else {
      setOpen(true)
    }
  }

  const validateTypeFileAndColor = (type_file_str, a, color_icons) => {
    let color = ''
    let icon = null
    if(type_file_str==='pdf') {
      color='red'
      icon=<FilePdfFilled style={{color:color_icons&&color, fontSize:color_icons&&'20px'}} />
    } else if(type_file_str==='excel'){
      color='green'
      icon=<FileExcelFilled style={{color:color_icons&&color, fontSize:color_icons&&'20px'}} />
    } else if(type_file_str==='word'){
      color='blue'
      icon=<FileWordFilled style={{color:color_icons&&color, fontSize:color_icons&&'20px'}} />
    } else if(type_file_str==='powerpoint'){
      color='orange'
      icon=<FilePptFilled style={{color:color_icons&&color, fontSize:color_icons&&'20px'}} />
    } else if(type_file_str==='image'){
      color='purple'
      icon=<FileImageFilled style={{color:color_icons&&color, fontSize:color_icons&&'20px'}} />
    }
    if(a){
      return {
        backgroundColor: color, borderColor: color
      }
    } else {

      return icon
    }
  }

  useEffect(()=> {
    
  }, [])

  return (
    <>
      <Modal style={{top:0}} width={'1300px'} 
        title={<> {validateTypeFileAndColor(element.type_file, false, true)} {element.description}</>} visible={open} 
        onCancel={toggleModal} footer={[]} >
          <UploadValueFile element={element} />
      </Modal>
      <Tooltip title={element.description}>
        <Button
          style={{ margin:'5px', borderRadius: "0px", ...validateTypeFileAndColor(element.type_file, true) }}
          icon={validateTypeFileAndColor(element.type_file, false)}
          type="primary"
          onClick={toggleModal}
        >
          {element.name}
        </Button>
      </Tooltip>
    </>
  );
};

export default SingleElement;

