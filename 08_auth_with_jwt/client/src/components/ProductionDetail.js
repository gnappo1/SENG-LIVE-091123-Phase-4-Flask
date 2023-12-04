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

  const handleDelete = () => {
    fetch(`/productions/${prod_id}`, {method: "DELETE"})
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