let lista_botones_apartar = document.querySelectorAll("#habitacionesDisponibles > div > div > div > div.col-md-4.offset-2 > div > button")

habitacionSeleccionada = -1

for(let i=0; i<lista_botones_apartar.length; i++){
    lista_botones_apartar[i].addEventListener('click', function(e){
        id = e.target.parentElement.parentElement.parentElement.parentElement.parentElement.id
        actualizarHabitacionSeleccionada(id)
    })
}

function actualizarHabitacionSeleccionada(id){
    if(habitacionSeleccionada == -1){
        document.querySelector("#contenedorHabitacionSeleccionada").innerHTML = '<div id="habitacionSeleccionada" class=" alert bg-dark text-light d-flex justify-content-between "> <div class="ms-2"> Número: <strong>002</strong> </div> <div> <button class="btn-danger btn">eliminar</button> </div> </div>'
        document.querySelector("#habitacionSeleccionada > div:nth-child(2) > button").addEventListener('click', function(){
            document.querySelector("#contenedorHabitacionSeleccionada").innerHTML = '';
            habitacionSeleccionada = -1
        })
    }
    habitacionSeleccionada = id
    document.querySelector("#habitacionSeleccionada > .ms-2 > strong").innerHTML = habitacionSeleccionada
}

function cambioFechaDesdeModal(){
    document.querySelector("body > main > section > div > div > div:nth-child(2) > div > div > form > div:nth-child(1) > input").value = document.querySelector("#modalAvailability > div > div > div.modal-body > div > div > div:nth-child(1) > div.container.mb-2 > div > div:nth-child(1) > input").value
}
function cambioFechaHastaModal(){
    document.querySelector("body > main > section > div > div > div:nth-child(2) > div > div > form > div.m-2.mt-3 > input").value = document.querySelector("#modalAvailability > div > div > div.modal-body > div > div > div:nth-child(1) > div.container.mb-2 > div > div:nth-child(2) > input").value
}
function cambioFechaDesdePrincipal(){
    document.querySelector("#modalAvailability > div > div > div.modal-body > div > div > div:nth-child(1) > div.container.mb-2 > div > div:nth-child(1) > input").value = document.querySelector("body > main > section > div > div > div:nth-child(2) > div > div > form > div:nth-child(1) > input").value
}
function cambioFechaHastaPrincipal(){
    document.querySelector("#modalAvailability > div > div > div.modal-body > div > div > div:nth-child(1) > div.container.mb-2 > div > div:nth-child(2) > input").value = document.querySelector("body > main > section > div > div > div:nth-child(2) > div > div > form > div.m-2.mt-3 > input").value
}

//setear minimo fecha

var today = new Date();
var dd = today.getDate();
var mm = today.getMonth() + 1; //January is 0!
var yyyy = today.getFullYear();
if (dd < 10) {
  dd = '0' + dd;
}
if (mm < 10) {
  mm = '0' + mm;
}
today = yyyy + '-' + mm + '-' + dd
document.querySelector("body > main > section > div > div > div:nth-child(2) > div > div > form > div:nth-child(1) > input").setAttribute("min",today);
document.querySelector("body > main > section > div > div > div:nth-child(2) > div > div > form > div.m-2.mt-3 > input").setAttribute("min",today);
document.querySelector("#modalAvailability > div > div > div.modal-body > div > div > div:nth-child(1) > div.container.mb-2 > div > div:nth-child(1) > input").setAttribute("min",today);
document.querySelector("#modalAvailability > div > div > div.modal-body > div > div > div:nth-child(1) > div.container.mb-2 > div > div:nth-child(2) > input").setAttribute("min",today);
document.querySelector("body > main > section > div > div > div:nth-child(2) > div > div > form > div:nth-child(1) > input").value = today
document.querySelector("body > main > section > div > div > div:nth-child(2) > div > div > form > div.m-2.mt-3 > input").value = today
document.querySelector("#modalAvailability > div > div > div.modal-body > div > div > div:nth-child(1) > div.container.mb-2 > div > div:nth-child(1) > input").value = today
document.querySelector("#modalAvailability > div > div > div.modal-body > div > div > div:nth-child(1) > div.container.mb-2 > div > div:nth-child(2) > input").value = today

async function obtenerCuartos(){
    fechaDesde = document.querySelector("body > main > section > div > div > div:nth-child(2) > div > div > form > div:nth-child(1) > input").value
    fechaHasta = document.querySelector("body > main > section > div > div > div:nth-child(2) > div > div > form > div.m-2.mt-3 > input").value
    url = "/room/"+fechaDesde+"/"+fechaHasta
    http://localhost:5000
    axios.get(url).then((response)=>{
        console.log(response.data.rows.length)
        if(response.data.rows.length==0){
            document.querySelector("#habitacionesDisponibles").innerHTML = '<div class="card card-body bg-danger">No hay habitaciones disponibles</div>'
        }else{
            let textoTemporal = ''
            for(let i=0; i<response.data.rows.length; i++){
                item = response.data.rows[i][0]
                textoTemporal = textoTemporal + '<div id="'+item+'" class="boton_habitacion_disponible"> <div class="container bg-dark text-light rounded-3 px-3 pt-1 mb-1"> <div class="row"> <div class="col-md-6"> <div class="row"> <div class="col"> <p>Número:</p> </div> <div class="col"> <strong>'+item+'</strong> </div> </div> <div class="row"> <div class="col"> <p>Disponibilidad actual:</p> </div> <div class="col"> <strong class="text-success">DISPONIBLE</strong> </div> </div> </div> <div class="col-md-4 offset-2"> <div class="d-flex justify-content-end me-4"> <button onclick="obtenerCuartos" class="btn btn-primary mt-3">Apartar</button> </div> </div> </div> </div> </div>'
            }
            document.querySelector("#habitacionesDisponibles").innerHTML = textoTemporal
            let lista_botones_apartar = document.querySelectorAll("#habitacionesDisponibles > div > div > div > div.col-md-4.offset-2 > div > button")

            for(let i=0; i<lista_botones_apartar.length; i++){
                lista_botones_apartar[i].addEventListener('click', function(e){
                    id = e.target.parentElement.parentElement.parentElement.parentElement.parentElement.id
                    actualizarHabitacionSeleccionada(id)
                })
            }
        }
    })

}

//reservar principal
document.querySelector("body > main > section > div > div > div:nth-child(2) > div > div > form > div.mx-2 > button").addEventListener('click', obtenerCuartos)

//reservar modal
document.querySelector("#modalAvailability > div > div > div.modal-body > div > div > div:nth-child(1) > div.container.mb-2 > div > button").addEventListener('click', obtenerCuartos)

document.querySelector("#modalAvailability > div > div > div.modal-body > div > div > div:nth-child(2) > div > button").addEventListener('click', function(){
    if(habitacionSeleccionada != -1){
        startDate = document.querySelector("body > main > section > div > div > div:nth-child(2) > div > div > form > div:nth-child(1) > input").value
        targetDate = document.querySelector("body > main > section > div > div > div:nth-child(2) > div > div > form > div.m-2.mt-3 > input").value
        id_room = habitacionSeleccionada
        
        let url = "http://localhost:5000/reservation"

        axios.post(url, {
            startDate,
            targetDate,
            id_room
        }).then((response)=>{
            alert(response.data.message)
            document.querySelector("#modalAvailability > div > div > div.modal-header > button").click()
        })
    }
})