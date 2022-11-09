import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from './containers/Login'
import Home from './containers/Home'
import Dga from './containers/Dga'
import Ssr from './containers/Ssr'
import Foot from './containers/Foot'


function App() {


  return (
    <>
       <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />          
        <Route path="/inicio" element={<Home />} />          
        <Route path="/dga" element={<Dga />} />          
        <Route path="/ssr" element={<Ssr />} />                  
        <Route path="/huella" element={<Foot />} />                  
      </Routes>
    </BrowserRouter>
    </>
  )
}

export default App;
