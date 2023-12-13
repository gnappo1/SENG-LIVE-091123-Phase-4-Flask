// 📚 Review With Students:
    // Request response cycle
    //Note: This was build using v5 of react-router-dom
import { Route, Switch, useHistory } from 'react-router-dom'
import {createGlobalStyle} from 'styled-components'
import {useEffect, useState, useCallback} from 'react'
import Home from './components/Home'
import ProductionForm from './components/ProductionForm'
import ProductionEdit from './components/ProductionEdit'
import Navigation from './components/Navigation'
import ProductionDetail from './components/ProductionDetail'
import Authentication from './components/Authentication'
import NotFound from './components/NotFound'
import "./App.css"


function App() {
  const [error, setError] = useState("");
  const [productions, setProductions] = useState([])
  const [production_edit, setProductionEdit] = useState(false)
  const [user, setUser] = useState(null);
  const history = useHistory()

  const updateUser = (user) => setUser(user)

  const handleNewError = useCallback((error) => {
    setError(error);
  }, []);

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
  const fetchProductions = () => {
    fetch("/productions")
    .then(response => {
      if (response.ok) {
        response.json().then(setProductions)
      } else {
        response.json().then(setError)
      }
    })
    .catch(setError)
  }

  useEffect(() => {
    if (!user) {
      //! ask the API if they know who we are with the jwt token from localStorage
      fetch("/me", {
        headers: {
          "Authorization": `Bearer ${localStorage.getItem("jwt_token")}` //! as specified in the docs
        }
      })
      .then(res => {
        if (res.ok) { //! token is valid
          res.json().then(updateUser).then(fetchProductions)
        } else if (res.status === 401) { //! token is invalid but maybe refresh token is still valid
          fetch("/refresh", {
            method: "POST",
            headers: {
              //! NOTICE HERE I send the refresh token since I know the access token is expired
              "Authorization": `Bearer ${localStorage.getItem("refresh_token")}`
            }
          })
          .then(res => {
            if (res.ok) { //! refresh token was still valid
              res.json().then(respObj => {
                //! update the user
                updateUser(respObj.user)
                //! update the expired token in localStorage with the newly created token coming from the API  
                localStorage.setItem("jwt_token", respObj.jwt_token)
              }).then(fetchProductions)
            } else {
              res.json().then(errorObj => handleNewError(errorObj.msg))
            }
          })
        } else { //! both tokens are invalid
          res.json().then(errorObj => handleNewError(errorObj.message || errorObj.msg))
        }
      })
      .catch(handleNewError)
    }
  }, [handleNewError, user])

  useEffect(() => {
    if (error) {
      const timeout = setTimeout(() => handleNewError(""), 3000)
      return () => {
        clearTimeout(timeout)
      };
    }
  }, [handleNewError, error]);

  const addProduction = (production) => setProductions(productions => [...productions, production])
  const updateProduction = (updated_production) => setProductions(productions => productions.map(production =>{
    if(production.id === updated_production.id){
      return updated_production
    } else {
      return production
    }
  } ))

  const deleteProduction = (deleted_production_id) => setProductions(productions => productions.filter((production) => production.id !== Number(deleted_production_id)) )

  const handleEdit = (production) => {
    setProductionEdit(production)
    history.push({pathname: `/productions/edit/${production.id}`, state:{production}})
  }


  if(!user) return (
    <>
      <GlobalStyle />
      <Navigation/>
      <div>{error}</div>
      <Authentication updateUser={updateUser} handleNewError={handleNewError} fetchProductions={fetchProductions}/>
    </>
  )
  return (
    <>
    <GlobalStyle />
    <Navigation updateUser={updateUser} user={user}/>
    <div>{error}</div>
      <Switch>
        <Route  path='/productions/new'>
          <ProductionForm addProduction={addProduction} handleNewError={handleNewError}/>
        </Route>
        <Route  path='/productions/edit/:id'>
          <ProductionEdit updateProduction={updateProduction} production_edit={production_edit} handleNewError={handleNewError}/>
        </Route>
        <Route path='/productions/:prod_id'>
            <ProductionDetail handleEdit={handleEdit} deleteProduction={deleteProduction} handleNewError={handleNewError}/>
        </Route>
        <Route exact path='/'>
          <Home  productions={productions} />
        </Route>
        <Route>
          <NotFound />
        </Route>
      </Switch>
    </>
  )
}

export default App

const GlobalStyle = createGlobalStyle`
    body{
      background-color: black; 
      color:white;
    }
    `
