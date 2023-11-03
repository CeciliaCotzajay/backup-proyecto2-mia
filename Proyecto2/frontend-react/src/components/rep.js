import React from 'react';


function Rep() {
  const apiUrl = process.env.REACT_APP_API_URL;

  const cargarReportes = async () => {
    try {
      const response = await fetch(apiUrl +'/cargaReportes', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 'command': '' }),
      });
      console.log("recibio en reportes")
      const data = await response.json();
      console.log(data)
      if (data.estado == "205") {
        console.log("confirmado si recibio en reportes")
        console.log(data.report)
      }else{
        console.log("error no reconocio algo en reportes o no hay paths")
      }
    } catch (error) {
        console.error("Error en la solicitud",error);
    }
  };



  return (
    <div className="col-12">
    <div className="card mt-4 text-warning bg-dark">
      <h5 className="card-header">
        <div className='d-flex justify-content-between'>
          <h4>Reportes</h4>
          <button className="btn btn-outline-primary">Logout</button>
        </div>
      </h5>
      <div className="card-body text-white">
        <div className="row align-items-start">
          <div className="col-11">
            <div className="row justify-content-center">
              <div className="col-2">
                  <button className="btn btn-outline-primary mt-3" onClick={cargarReportes}>Cargar Reportes</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  );
}

export default Rep;