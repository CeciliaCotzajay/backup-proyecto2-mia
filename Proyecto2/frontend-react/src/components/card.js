import React, { useState, useRef } from 'react';

function Card() {

    const [results, setResults] = useState('');
    const [commands, setCommands] = useState('');
    const [isPaused, setIsPaused] = useState(false);
    const [commands_list, setCommands_list] = useState([]);
    const textAreaRef = useRef(null);
    const apiUrl = process.env.REACT_APP_API_URL;

  
    const handleFileChange = (e) => {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = (event) => {
        setCommands(event.target.result);
      };
      if (file) {
        reader.readAsText(file);
      }
    };

    const handleTextAreaKeyPress = (event) => {
        if (event.key === 'Enter') {
            if(isPaused){
                sendCommands(commands_list);
            }
        }
    };

    const sendCommands = async (commands) => {
        for (let i = 0; i < commands.length; i++) {
            const command = commands[i].trim();
            if (command) { // Evita enviar líneas en blanco
                setCommands_list(commands.slice(i+1, commands.length));
                if(command == 'pause'){
                    setIsPaused(true);
                    console.log(commands_list);
                    setResults(prevResults => prevResults + `[Pause] => Presiona Enter para continuar\n`);
                    break;
                }
                try {
                    const response = await fetch(apiUrl +'/execute', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ command }),
                    });
                    const data = await response.json();
                    console.log(data)
                    console.log("rrrrrrrr")
                    console.log(data.mensaje)
                    console.log("dddddddd")
                    setResults(prevResults => prevResults + `${data.mensaje}\n`);
                    if (data.estado == "201") {
                        console.log("si")
                        var resultado = window.confirm('¿Está seguro de eliminar el disco? \n Por favor confirme...');
                        if (resultado === true) {
                            enviarConfirmacion(command+" -resp=si");
                        } else { 
                            enviarConfirmacion(command+" -resp=no");
                        }
                    }
                } catch (error) {
                    console.error(`Error en la solicitud ${i + 1}: ${error}`);
                }
            }
        }
    };

    const handleSubmit = () => {
        //Para enfocar el textarea
        textAreaRef.current.focus();
        //Para limpiar el textarea
        setResults('');
        //Para dividir los comandos por salto de línea
        const commandLines = commands.split('\n');
        //Actualizamos la lista de comandos y enviamos los comandos
        setCommands_list(commandLines);
        sendCommands(commandLines);
    };

    const enviarConfirmacion = async (resp) => {
        try {
            console.log("envio correcto")
            console.log(resp)
            const response = await fetch(apiUrl +'/resp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'command': resp }),
            });
            console.log("recibio")
            const data = await response.json();
            console.log(data)
            if (data.estado == "202") {
                console.log("eliminado")
                window.alert('>>Disco eliminado exitosamente...');
            }else{
                window.alert('>>ELiminación cancelada..');
            }
            setResults(prevResults => prevResults + `${data.mensaje}\n`);
        } catch (error) {
            console.error("Error en la solicitud");
        }
    };

  return (
    <div className="card mt-4 text-info bg-dark">
      <h5 className="card-header">
        <div className='d-flex justify-content-between'>
            <h4>Manejo de Archivos</h4>
            <div>
                <input className="form-control" type="file" id="formFile" onChange={handleFileChange}></input>
            </div>
        </div>
      </h5>
      <div className="card-body text-white">
        <div className="d-flex flex-row-reverse">
        </div>
        <div className="row align-items-start">
            <div className="col">
                <div className="mb-3">
                    <label className="form-label">Comandos a enviar</label>
                    <textarea
                        className="form-control" 
                        placeholder="Escribe aquí tus comandos" 
                        style={{height: 300}}
                        value={commands}
                        onChange={(e) => setCommands(e.target.value)}
                    ></textarea>
                </div>
            </div>
            <div className="col">
                <div className="mb-3">
                    <label className="form-label">Consola de salida</label>
                    <textarea 
                        className="form-control" 
                        placeholder="Aquí aparecerán los resultados" 
                        readOnly
                        ref={textAreaRef}
                        style={{height: 300}} 
                        value={results}
                        onKeyDown={handleTextAreaKeyPress}
                    ></textarea>
                </div>
            </div>
        </div>
        <div className="row justify-content-center">
            <div className="col-2">
                <button className="btn btn-outline-primary mt-3" onClick={handleSubmit}>Enviar</button>
            </div>
        </div>
      </div>
    </div>
  );
}

export default Card;