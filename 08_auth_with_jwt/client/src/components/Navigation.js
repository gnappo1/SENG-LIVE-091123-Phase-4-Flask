import { useState } from 'react'
import {Link} from 'react-router-dom'
import styled from 'styled-components'
import { useHistory } from 'react-router-dom'
import { GiHamburgerMenu } from 'react-icons/gi'

function Navigation({updateUser, user, handleNewError}) {
 const [menu, setMenu] = useState(false)
//  const history = useHistory()

 const handleLogout = () => {
    //! No need to send a request to the API
    //! There is nothing our API can currently do to invalidate this token
    //! the frontend simply has to remove the tokenS (as in both of them) from localStorage 
    localStorage.removeItem("jwt_token")
    localStorage.removeItem("refresh_token")
    updateUser(null)
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
                  <li><Link to='/'> Login/Signup</Link></li>
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
