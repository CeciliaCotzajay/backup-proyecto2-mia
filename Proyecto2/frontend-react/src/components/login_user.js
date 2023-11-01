import React from 'react';


function Login_user() {
  return (
    <div className="col-6">
    <div className="card mt-4 text-warning bg-dark">
      <h5 className="card-header">
        <div className='d-flex justify-content-between'>
          <h4>Inicio de Sesión</h4>
        </div>
      </h5>
      <div className="card-body text-white">
        <div className="row align-items-start">
          <div className="col-11">
            <div className="mb-3">
              <form>
                <div className="mb-3">
                  <label for="exampleInputEmail1" className="form-label">User</label>
                  <input type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder='Ingresa tu user'></input>
                  <div id="emailHelp" className="form-text">We'll never share your email with anyone else.</div>
                </div>
                <div className="mb-3">
                  <label for="exampleInputPassword1" className="form-label">Password</label>
                  <input type="password" className="form-control" id="exampleInputPassword1" placeholder='Ingresa tu password'></input>
                </div>
                <br></br>
                <center>
                <button type="submit" className="btn btn-outline-primary">Cancelar</button>
                <button type="submit" className="btn btn-outline-success">Loguear</button>
                </center>
			        </form>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  );
}

export default Login_user;