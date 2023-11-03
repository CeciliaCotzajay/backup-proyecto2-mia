import React, { useState } from 'react';


function Rep() {
  const [imageUrl, setimageUrl] = useState([]);
  const [otroDic, setotroDic] = useState({});
  const apiUrl = process.env.REACT_APP_API_URL;
  const urlImage = process.env.REACT_IMG_URL;

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
        window.alert('>>Reportes generados exitosamente...');
        console.log(data.report)
        setotroDic(data.report)
        console.log(otroDic)
      }else{
        window.alert('>>Ocurrio un error al cargar reportes...');
        console.log("error no reconocio algo en reportes o no hay paths")
      }
    } catch (error) {
        console.error("Error en la solicitud",error);
    }
  };

  const guardarUrls = () => {
    let claves = Object.keys(otroDic);
    console.log(claves)
    for (let i = 0; i < claves.length; i++) {
      claves[i] = urlImage + '/'+claves[i]; 
    }
    setimageUrl(claves)
    console.log(imageUrl)
    console.log("deberia verse la imagenes")
};

  return (
    <div className="col-12">
    <div className="card mt-4 text-warning bg-dark">
      <h5 className="card-header">
        <div className='d-flex justify-content-between'>
          <h4>Reportes</h4>
          <div className="col-2">
            <button className="btn btn-outline-primary mt-3" onClick={cargarReportes}>Cargar Reportes</button>
            <button className="btn btn-outline-success mt-3" onClick={guardarUrls}>Visualizar Reportes</button>
          </div>
          <button className="btn btn-outline-warning">Logout</button>
        </div>
      </h5>
      <div className="card-body text-white">
        <div className="row align-items-start">
          <div className="col-11">
            <div className="row justify-content-center">
              <div className="col-2">
                <div>
                  {imageUrl.map((imagen, index) => (
                    <img key={index} src={imagen} alt={`Imagen ${index + 1}`} width={200} height={200}/>
                  ))}
                </div>
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