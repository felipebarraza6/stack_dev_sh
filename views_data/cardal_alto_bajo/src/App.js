// React
import React from 'react'

// Auth Reducers
import { login_reducer } from './reducers/auth.js'

// Containers
import Home from './containers/Home'
import Login from './containers/Login'

// Create Contexts
export const AuthContext = React.createContext()


const initialState = {
  isAuthenticated: false,  
  access_token: null,
  user: null
}


function App(){
  
  const [state, dispatch] = React.useReducer(login_reducer, initialState)
  
  React.useEffect(() => {

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

  return(
    
    <AuthContext.Provider
    
      value = {{
        state,
        dispatch
      }}
    > 
    {state.isAuthenticated ?
      <Home />:
      <Login />
    }

      
    
    </AuthContext.Provider>
    
    
  )
    
 
}

export default App;
