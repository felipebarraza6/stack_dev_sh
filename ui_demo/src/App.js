import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from './containers/Login'
import Home from './containers/Home'
import Dga from './containers/Dga'
import Ssr from './containers/Ssr'
import Foot from './containers/Foot'
import HomeM from './containers/HomeM'
import HomeC from './containers/HomeC'


function App() {


  return (
    <>
       <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />          
        <Route path="/inicio" element={<Home />} />          
        <Route path="/dga" element={<Dga />} />          
        <Route path="/ssr" element={<Ssr />} />                  
        <Route path="/huella" element={<Foot />} />                  
        <Route path="/mide" element={<HomeM />} />
        <Route path="/construccion" element={<HomeC />} />
      </Routes>
    </BrowserRouter>
    </>
  )
}

export default App;
