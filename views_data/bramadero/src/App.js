import React, { useReducer, useEffect, createContext } from 'react'

import { reducer } from './reducers/Auth'

import AuthLayout from "layouts/Auth/Auth.js"
import AdminLayout from "layouts/Admin/Admin.js"

export const AuthContext = createContext()


function App(props) {

  const initialState = {
    isAuthenticated: false,
    access_token: null,
    user: null
  }

  const [state, dispatch] = useReducer(reducer, initialState)

  useEffect(() => {

    const access_token = JSON.parse(localStorage.getItem('access_token') || null)
    const user = JSON.parse(localStorage.getItem('user') || null)

    if(user && access_token){
      dispatch({
        type: 'LOGIN',
        payload: {
          access_token,
          user
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
        {state.isAuthenticated ? 
            <AdminLayout {...props} />
            :
            <AuthLayout {...props} />  
        }
      </div>

    </AuthContext.Provider>

  )

}

export default App
