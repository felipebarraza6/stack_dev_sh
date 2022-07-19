
import RegularTables from "./views/tables/RegularTables.js";

import Charts from "./views/Charts.js";
import Charts2 from "./views/Charts2.js";
import Dashboard from "./views/Dashboard.js";
import MiPozo from "./views/MiPozo.js";
const user = JSON.parse(localStorage.getItem('user'))

const routes = []

const validateUser = () => {
  if(user.username==='avicolaelmonte'){
   routes.push({
    path: "/dashboard",
    name: "MI POZO",
    icon: "tim-icons icon-compass-05",
    component: MiPozo,
    layout: "/admin",
  })   
  } else {
    routes.push({
      path: "/dashboard",
      name: "INICIO",
      icon: "tim-icons icon-components",
      component: Dashboard,
      layout: "/admin",
    })
    routes.push({
      path: "/mipozo",
      name: "MI POZO",
      icon: "tim-icons icon-compass-05",
      component: MiPozo,
      layout: "/admin",
    })
    routes.push({
      path: "/charts",
      name: "GRAFICOS",
      rtlName: "الرسوم البيانية",
      icon: "tim-icons icon-chart-bar-32",
      component: Charts,
      layout: "/admin",
    })
    routes.push({
      path: "/anatyc-data",
      name: "ANALISIS DE DATOS",
      rtlName: "الرسوم البيانية",
      icon: "tim-icons icon-molecule-40",
      component: Charts2,
      layout: "/admin",
    })
    routes.push({
      path: "/dga",
      name: "DGA",
      rtlName: "الرسوم البيانية",
      icon: "tim-icons icon-bullet-list-67",
      layout: "/dga",
    })
    routes.push({
      path: "/reports",
      name: "REPORTES",
      rtlName: "الرسوم البيانية",
      icon: "tim-icons icon-bullet-list-67",
      component: RegularTables,
      layout: "/admin",
     })
  }  

}

validateUser()


export default routes;
