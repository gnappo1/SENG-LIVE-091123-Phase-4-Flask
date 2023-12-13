import  {useParams, useHistory } from 'react-router-dom'
import {useEffect, useState} from 'react'
import styled from 'styled-components'
import NotFound from './NotFound'

function ProductionDetail({handleEdit, deleteProduction, handleNewError}) {
  const [production, setProduction] = useState({crew_members:[]})
  // const [error, setError] = useState(null)
  //Student Challenge: GET One 
  const {prod_id} = useParams()
  const history = useHistory()

  useEffect(()=>{
    fetch(`/productions/${prod_id}`)
    .then(response => {
      if (response.ok){ //! if it's in 200-299 range
        response.json().then(setProduction)
      } else {
        response.json().then(errorObj => handleNewError(errorObj.message))
      }
    })
    .catch(handleNewError)
  },[prod_id, handleNewError])

  const checkToken = () => fetch("/check", {
    headers: {
      //! NOTICE HERE I send the refresh token since I know the access token is expired
      "Authorization": `Bearer ${localStorage.getItem("jwt_token")}`
    }
  })

  const postRefreshToken = () => {
    return fetch("/refresh", {
      method: "POST",
      headers: {
        //! NOTICE HERE I send the refresh token since I know the access token is expired
        "Authorization": `Bearer ${localStorage.getItem("refresh_token")}`
      }
    })
  }

  const deleteFetchProduction = () => {
    return fetch(`/productions/${prod_id}`, {
      method: "DELETE",
      headers: {
        'Authorization': `Bearer ${localStorage.getItem("jwt_token")}`
      }
    })
    .then(response => {
      if (response.ok){ //! 204
        deleteProduction(prod_id)
        history.push("/")
      } else {
        response.json().then(errorObj => handleNewError(errorObj.message))
      }
    })
    .catch(handleNewError)
  }

  const handleDelete = () => {
    checkToken() //! make sure token is still valid
    .then(resp => {
      if (resp.ok) {
        deleteFetchProduction() //! try to fire a DELETE with a valid token
      } else if (resp.status === 401) { //! token is invalid but maybe refresh token is still valid
        postRefreshToken() //! try to refresh the token
        .then(res => {
          if (res.ok) { //! refresh token was still valid
            res.json().then(respObj => {
              //! update the expired token in localStorage with the newly created token coming from the API  
              localStorage.setItem("jwt_token", respObj.jwt_token)
            })
            .then(deleteFetchProduction) //! try again to fire the DELETE now that a new token has been issued
          } else {
            res.json().then(errorObj => handleNewError(errorObj.msg))
          }
        })
      }
    })
    .catch(err => handleNewError(err))
  }

  if (!production.id) {
    return <NotFound />
  }
  const {id, title, genre, image,description, crew_members} = production 
  // if(error) return <h2>{error}</h2>
  return (
      <CardDetail id={id}>
        <h1>{title}</h1>
          <div className='wrapper'>
            <div>
              <h3>Genre:</h3>
              <p>{genre}</p>
              <h3>Description:</h3>
              <p>{description}</p>
              <h2>Cast Members</h2>
              <ul>
                {crew_members.map(cast => <li key={cast.id}>{`${cast.role} : ${cast.name}`}</li>)}
              </ul>
            </div>
            <img src={image} alt={title}/>
          </div>
      <button onClick={()=> handleEdit(production)} >Edit Production</button>
      <button onClick={handleDelete} >Delete Production</button>

      </CardDetail>
    )
  }
  
  export default ProductionDetail
  const CardDetail = styled.li`
    display:flex;
    flex-direction:column;
    justify-content:start;
    font-family:Arial, sans-serif;
    margin:5px;
    h1{
      font-size:60px;
      border-bottom:solid;
      border-color:#42ddf5;
    }
    .wrapper{
      display:flex;
      div{
        margin:10px;
      }
    }
    img{
      width: 300px;
    }
    button{
      background-color:#42ddf5;
      color: white;
      height:40px;
      font-family:Arial;
      font-size:30px;
      margin-top:10px;
    }
  `