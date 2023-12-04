import { useState } from 'react'
import {Link} from 'react-router-dom'
import styled from 'styled-components'
import { useHistory } from 'react-router-dom'
import { GiHamburgerMenu } from 'react-icons/gi'

function Navigation({updateUser, user, handleNewError}) {
 const [menu, setMenu] = useState(false)
//  const history = useHistory()

 const handleLogout = () => {
    //! What do we do here?
    fetch("/logout", {method: "DELETE"})
    .then(() => {
      updateUser(null)
      localStorage.removeItem("jwt_token")
    })
    .catch(handleNewError)
 }

    return (
        <Nav> 
          <NavH1>Flatiron Theater Company</NavH1>
          <Menu>
            {!menu?
              <div onClick={() => setMenu(!menu)}>
                <GiHamburgerMenu size={30}/> 
              </div>:
              <ul>
                <li onClick={() => setMenu(!menu)}>x</li>
                { user ? (
                  <>
                    <li><Link to='/productions/new'>New Production</Link></li>
                    <li><Link to='/'> Home</Link></li>
                    <li onClick={handleLogout}> Logout </li>
                  </>

                ) : (
                  <li><Link to='/authentication'> Login/Signup</Link></li>
                )}
              </ul>
            }
          </Menu>

        </Nav>
    )
}

export default Navigation


const NavH1 = styled.h1`
font-family: 'Splash', cursive;
`
const Nav = styled.div`
  display: flex;
  justify-content:space-between;
  
`;

const Menu = styled.div`
  display: flex;
  align-items: center;
  a{
    text-decoration: none;
    color:white;
    font-family:Arial;
  }
  a:hover{
    color:pink
  }
  ul{
    list-style:none;
  }
  
`;
