
import RegularTables from "./views/tables/RegularTables.js";

import Charts from "./views/Charts.js";
import Charts2 from "./views/Charts2.js";
import Dashboard from "./views/Dashboard.js";
import MiPozo from "./views/MiPozo.js";




const routes = [
  {
    path: "/dashboard",
    name: "INICIO",
    icon: "tim-icons icon-components",
    component: Dashboard,
    layout: "/admin",
  },
  {
    path: "/mipozo",
    name: "MI POZO",
    icon: "tim-icons icon-compass-05",
    component: MiPozo,
    layout: "/admin",
  },
  {
    path: "/charts",
    name: "GRAFICOS",
    rtlName: "الرسوم البيانية",
    icon: "tim-icons icon-chart-bar-32",
    component: Charts,
    layout: "/admin",
  },
  {
    path: "/anatyc-data",
    name: "ANALISIS DE DATOS",
    rtlName: "الرسوم البيانية",
    icon: "tim-icons icon-molecule-40",
    component: Charts2,
    layout: "/admin",
  },
  {
    path: "/dga",
    name: "DGA",
    rtlName: "الرسوم البيانية",
    icon: "tim-icons icon-bullet-list-67",
    layout: "/dga",
  },

  {
    path: "/reports",
    name: "REPORTES",
    rtlName: "الرسوم البيانية",
    icon: "tim-icons icon-bullet-list-67",
    component: RegularTables,
    layout: "/admin",
  },
]

export default routes;
