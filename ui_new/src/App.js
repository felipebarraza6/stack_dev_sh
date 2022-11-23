import React, { createContext, useReducer, useEffect } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom"

import { appReducer } from './reducers/appReducer'
import sh from './api/sh/endpoints'



import Login from './containers/Login'
import Home from './containers/Home'
import Dga from './containers/Dga'
import Ssr from './containers/Ssr'
import Foot from './containers/Foot'

export const AppContext = createContext()


function App() {

  const initialState = {
    isAuth: false,
    token: null,
    user: null,
    profile_client: null,
    selected_profile: null
  }

  const [state, dispatch] = useReducer(appReducer, initialState)
  
  const updateApp = async() => {
    const token = JSON.parse(localStorage.getItem('token') || null)
    const user = JSON.parse(localStorage.getItem('user') || null)
    const profile_client = JSON.parse(localStorage.getItem('profile_client') || null)
    const selected_profile = JSON.parse(localStorage.getItem('selected_profile') || null)
    
     
    if(user && token && profile_client){
      const rq = await sh.get_profile().then((x)=>{        
        dispatch({
          type: 'UPDATE',
          payload: {
            token: token,
            user: x.user,
            profile_data: x.user.profile_data,
            selected_profile: selected_profile
          }
        })
      })    
      return rq  
    } else {   
      window.open('/')   
    }
  }

  useEffect(()=> {
    updateApp()
  }, [])

  return (
    <AppContext.Provider value={{ state, dispatch }}>      
       
        {state.isAuth ? <Home />:
          <Login />}      
    </AppContext.Provider>
  )
}

export default App
