import React from "react"
import ReactDOM from "react-dom"
import { BrowserRouter, Route, Switch } from "react-router-dom"


import "./assets/css/nucleo-icons.css"
import "react-notification-alert/dist/animate.css"
import "./assets/scss/black-dashboard-pro-react.scss?v=1.2.0"
import "./assets/demo/demo.css"
import App from './App'

ReactDOM.render(
  <BrowserRouter>
    <Switch>
      <Route path="/" render={(props) => <App {...props} />} />    
    </Switch>
  </BrowserRouter>,
  document.getElementById("root")
)
