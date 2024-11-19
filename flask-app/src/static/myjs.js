function mostrarDatos(lugar, datos){

    let cTabla = "<table border=2 class='table table-dark'><tr class='sombreado'><th>Correo</th><th>Nombre</th><th>Apellido</th><th>Borrar</th></tr>";
    datos.forEach(element => {
        cTabla += `<tr><td>${element.email}</td><td>${element.nombre}</td><td>${element.apellido}</td><td><input class="btn btn-danger btn-lg" type="button" value="Eliminar" onclick="eliminarUsuario('${element.email}');"></td></tr>`;        
    });
    cTabla += "</tbody></table>";

    let destino=document.getElementById(lugar);
    destino.innerHTML=cTabla;
}

function cargarUsuarios(){

    /* obtener usuarios */
    fetch("/usuarios")
    .then(response => response.json())
    .then(data => {
        console.log(data);
        mostrarDatos("grilla",data.rdo);

    });

}


function eliminarUsuario(email){

    /* obtener usuarios */
    console.log(email)
    fetch(`/usuarios/${email}`,{
        method:"DELETE"
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        alert("dato eliminado");
        cargarUsuarios();
    });

}


let formNuevoUsuario = document.getElementById("nuevoUsuario");
formNuevoUsuario.addEventListener("submit", event => {
    event.preventDefault();

    // Agrego un usuarios

    let data = new FormData(formNuevoUsuario);
    // Convert form data to a regular object (optional)
    const formObject = {};
    data.forEach((value, key) => {
        formObject[key] = value;
    });

    console.log(formObject);

    fetch('/usuarios', { 
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formObject)
    })
    .then(response => response.json())
    .then(data => {
            console.log(data);
    });
    
});
