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
      fetch("/me")
      .then(res => {
        if (res.ok) {
          res.json().then(updateUser).then(fetchProductions)
        } else if (res.status === 401) {
          fetch("/refresh", {
            method: "POST",
            headers: {
              'X-CSRF-TOKEN': getCookie('csrf_refresh_token'),
            }
          })
          .then(res => {
            if (res.ok) {
              res.json().then(updateUser).then(fetchProductions)
            } else {
              res.json().then(errorObj => handleNewError(errorObj.msg))
            }
          })
        } else {
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
