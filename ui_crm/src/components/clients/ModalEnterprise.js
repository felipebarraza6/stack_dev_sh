import React from 'react'

import { Modal, Descriptions, Badge, Tag } from 'antd'

import { BuildOutlined } from '@ant-design/icons'

import moment from 'moment'

const ModalEnterprise = (data) =>{
    
    let date_jurisdiction = moment(data.date_jurisdiction).add(1,'year')   
    let today = moment()

    const diff_days = date_jurisdiction.diff(today, 'days')
    const diff_weeks = date_jurisdiction.diff(today, 'weeks')
    const diff_months = date_jurisdiction.diff(today, 'months')
    const diff_years = date_jurisdiction.diff(today, 'years')

    const difference = `${date_jurisdiction.format('YYYY-MM-DD')} ( ${diff_years} Años | ${diff_months} Meses | ${diff_weeks} Semanas | ${diff_days} Días ) para la renovación de directorio`
 
    Modal.info({
        title: <>{data.name} {data.is_active ? <Badge style={{float: 'right'}} status="processing" text="Activo" />:<Badge style={{float: 'right'}} color='red' status="processing" text="Inactivo" /> } </>,
        icon: <BuildOutlined style={{ color: '#1890ff'}}/>,

        content: 
            <React.Fragment>
            
                {data.name ? <Tag style={{margin:'3px'}} color="green">Nombre</Tag>: <Tag color="red">Nombre</Tag>}
                {data.rut ? <Tag style={{margin:'3px'}} color="green">Rut</Tag>: <Tag color="red">Rut</Tag>}
                {data.type_client ? <Tag color="green">Tipo de Cliente</Tag>: <Tag color="red">Tipo de Cliente</Tag>}
                {data.phone_number ? <Tag color="green">Número de telefono</Tag>: <Tag color="red">Número de telefono</Tag>}
                {data.email ? <Tag color="green">Email</Tag>: <Tag color="red">Email</Tag>}

                {data.region ? <Tag color="green">Región</Tag>: <Tag color="red">Región</Tag>}
                {data.province ? <Tag color="green">Provincia</Tag>: <Tag color="red">Provincia</Tag>}
                {data.commune ? <Tag color="green">Comuna</Tag>: <Tag color="red">Comuna</Tag>}
                {data.address_exact ? <Tag color="green">Ubicación exacta</Tag>: <Tag color="red">Ubicación exacta</Tag>}

                {data.type_client === 'Empresa' &&
                    <>
                        {data.amount_regularized ? <Tag color="green">Derechos regularizados</Tag>: <Tag color="red">Derechos regularizados</Tag>}
                        {data.flow_rates ? <Tag color="green">Caudales</Tag>: <Tag color="red">Caudales</Tag>}
                        {data.category ? <Tag color="green">Categoría</Tag>: <Tag color="red">Categoría</Tag>}
                    </>  
                }

                {data.type_client === 'Planta APR' &&
                    <>
                        {data.administered ? <Tag color="green">Tipo organización</Tag>: <Tag color="red">Derechos regularizados</Tag>}
                        {data.number_starts ? <Tag color="green">Cantidad de Arranques</Tag>: <Tag color="red">Cantidad de Arranques</Tag>}
                        {data.date_jurisdiction ? <Tag color="green">Fecha de Constitución</Tag>: <Tag color="red">Fecha de Constitución</Tag>}
                    </>  
                }
            
            <Descriptions style={{marginTop:'60px'}} title="General" bordered>
                <Descriptions.Item label="Nombre">{data.name ? data.name : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="RUT">{data.rut ? data.rut : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="Tipo Cliente">{data.type_client ? data.type_client : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="Telefono">{data.phone_number ? data.phone_number : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="Email">{data.email ? data.email : 'S/D'}</Descriptions.Item>
            </Descriptions>

            <Descriptions style={{marginTop:'30px'}} title="Ubicación" bordered>
                <Descriptions.Item label="Región">{data.region ? data.region : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="Provincia">{data.province ? data.province : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="Comuna">{data.commune ? data.commune : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="Ubicación exacta">{data.address_exact ? data.address_exact : 'S/D'}</Descriptions.Item>                
            </Descriptions>
            
            {data.type_client === 'Empresa' &&
            
            <Descriptions style={{marginTop:'30px'}} title="Datos de Empresa" bordered>
                <Descriptions.Item label="Derechos Regularizados">{data.amount_regularized ? data.amount_regularized : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="Caudales">{data.flow_rates ? data.flow_rates : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="Categoría">{data.category ? data.category : 'S/D'}</Descriptions.Item>                
            </Descriptions>
            
            }

            {data.type_client === 'Planta APR' &&
            <Descriptions style={{marginTop:'30px'}} title="Datos de Planta APR" bordered>
                <Descriptions.Item label="Derechos Regularizados">{data.administered ? data.administered : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="Cantidad de arranques">{data.number_starts ? data.number_starts : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="Fecha de Constitución">{data.date_jurisdiction ? data.date_jurisdiction : 'S/D'}</Descriptions.Item>
                <Descriptions.Item label="Fecha de renovación de directorio">{data.date_jurisdiction ? difference : 'S/D'}</Descriptions.Item>                
            </Descriptions>
            }
            </React.Fragment>,

        okText: 'Cerrar',                        
        width: '1300px'      
    })
}

export default ModalEnterprise