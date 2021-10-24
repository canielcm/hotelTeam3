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