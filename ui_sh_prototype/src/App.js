import React, { useReducer, useEffect, createContext } from 'react'

import { reducer } from './reducers/Auth.js'

import AuthLayout from "./layouts/Auth/Auth.js"
import AdminLayout from "./layouts/Admin/Admin.js"
import api_crm from './api_crm/endpoints.js'

export const AuthContext = createContext()


function App(props) {

  const initialState = {
    isAuthenticated: false,
    access_token: null,
    user: null
  }

  const [state, dispatch] = useReducer(reducer, initialState)

  useEffect( async() => {

    document.body.classList.toggle('white-content')

    const access_token = JSON.parse(localStorage.getItem('access_token') || null)
    const user = JSON.parse(localStorage.getItem('user') || null)
    const token_novus = localStorage.getItem('token_novus')
    
    const rq = await api_crm.retrieve_user(user.username)

    if(user && access_token){
      dispatch({
        type: 'LOGIN_A',
        payload: {
          access_token,
          'update_data':rq,
          user,
        }
      })
    }
    

      }, [])


  return (

    <AuthContext.Provider
      value={{
        state,
        dispatch
      }}
    >
      <div className="App" style={{backgroundColor:'#030852'}}>
        {!state.isAuthenticated ? 
          <AuthLayout {...props} /> : <AdminLayout {...props} />
        }
      </div>

    </AuthContext.Provider>

  )

}

export default App
