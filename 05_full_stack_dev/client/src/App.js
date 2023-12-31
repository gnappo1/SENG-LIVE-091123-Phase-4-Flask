// 📚 Review With Students:
    // Request response cycle
    //Note: This was build using v5 of react-router-dom
import { Route, Switch, useHistory } from 'react-router-dom'
import {createGlobalStyle} from 'styled-components'
import {useEffect, useState} from 'react'
import Home from './components/Home'
import ProductionForm from './components/ProductionForm'
import ProductionEdit from './components/ProductionEdit'
import Navigation from './components/Navigation'
import ProductionDetail from './components/ProductionDetail'
import NotFound from './components/NotFound'
import "./App.css"
function App() {
  const [error, setError] = useState("");
  const [productions, setProductions] = useState([])
  const [production_edit, setProductionEdit] = useState(false)
  const history = useHistory()
  //5.✅ GET Productions
  useEffect(() => {
    fetch("/productions")
    .then(response => response.json())
    .then(setProductions)
    .catch(setError)
  }, [])
  // 6.✅ navigate to client/src/components/ProductionForm.js

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

  const handleNewError = (error) => {
    setError(error)
  }
  return (
    <>
    <GlobalStyle />
    <Navigation handleEdit={handleEdit}/>
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
