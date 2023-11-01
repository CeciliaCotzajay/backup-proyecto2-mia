import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import Nav from './components/navbar';
import Card from './components/card';
import Login_user from './components/login_user';
import Rep from './components/rep';

function App() {
  return (
    <Router>
      <Nav />
      <div className='container'>
        <Routes>
          <Route exact path='/' element={<Card/>}/>
          <Route exact path='/login' element={<Login_user/>}/>
          <Route exact path='/reportes' element={<Rep/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
