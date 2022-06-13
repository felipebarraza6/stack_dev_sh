/*!

=========================================================
* Black Dashboard PRO React - v1.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/black-dashboard-pro-react
* Copyright 2020 Creative Tim (https://www.creative-tim.com)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
/*eslint-disable*/
import React from "react";
import { Container, Row } from "reactstrap";
// used for making the prop types of this component
import PropTypes from "prop-types";

const Footer = (props) => {
  return (
    <footer className={"footer" + (props.default ? " footer-default" : "")}>
      <Container fluid={props.fluid ? true : false}>
        <ul className="nav">
          <li className="nav-item">
            
          </li>{" "}
          <li className="nav-item">
           
          </li>{" "}
          <li className="nav-item">
            
          </li>
        </ul>
        <div className="copyright">
          © {new Date().getFullYear()} Desarrollado con {" "}
          <i className="tim-icons icon-heart-2" /> por{" "}
          <a href="https://www.smarthydro.cl/" target="_blank">
            Smart Hydro / Departamento IOT
          </a>{" "}          
        </div>
      </Container>
    </footer>
  );
};

Footer.propTypes = {
  default: PropTypes.bool,
  fluid: PropTypes.bool,
};

export default Footer;
