import React from 'react';
import {Link} from 'react-router-dom'

function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <Link to='/'>
            <img src='./img-production/icon-archi.webp' width='50' height='50'></img>
        </Link>
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNavDropdown">
            <ul className="navbar-nav m-auto">
                <li className="nav-item">
                    <Link className="nav-link" to="/">   Inicio</Link>
                </li>
                <li className="nav-item">
                    <Link className="nav-link" to="/login">Login</Link>
                </li>
                <li className="nav-item">
                    <Link className="nav-link" to="/reportes">Reportes</Link>
                </li>
            </ul>
        </div>
    </nav>
  );
}

export default Navbar;