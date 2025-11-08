// Referencias
    const btnSlide = document.getElementById("slide-btn");
    const slideTitle = document.getElementById("slide-title");
    const slideText = document.getElementById("slide-text");
    const registroSection = document.getElementById("registro-section");
    const loginSection = document.getElementById("login-section");
    const slidePanel = document.getElementById("slide-panel");
    let panelState = "login"; // login / registro

    // Cambia entre login y registro visualmente
    btnSlide.addEventListener('click', ()=>{
      if(panelState==="login"){
        // Mostrar registro
        loginSection.classList.add('hidden');
        registroSection.classList.remove('hidden');
        slideTitle.textContent = "¡Hola!";
        slideText.textContent = "¿Ya tienes cuenta? Ingresa tus datos para acceder a todas las funciones.";
        btnSlide.textContent = "Iniciar Sesión";
        panelState = "registro";
        slidePanel.style.background = "linear-gradient(120deg,#3AB397 40%,#53e0c6 100%)";
      }else{
        // Mostrar login
        registroSection.classList.add('hidden');
        loginSection.classList.remove('hidden');
        slideTitle.textContent = "¡Bienvenido!";
        slideText.textContent = "¿Eres nuevo aquí? Regístrate para usar todas las funciones del sitio.";
        btnSlide.textContent = "Registrarse";
        panelState = "login";
        slidePanel.style.background = "linear-gradient(120deg,#3AA8AD 70%,#53e0c6 100%)";
      }
    });

const userForm = document.querySelector('#registro-form') //selecciona el formulario por su id

let users = [] //arreglo para almacenar los usuarios

window.addEventListener('DOMContentLoaded', async ()=> {
    const response = await fetch('/dato/api') //ruta de la API para obtener los usuarios
    const data = await response.json()
    users = data //almacena los usuarios en el arreglo
    renderUsers(users) //llama a la funcion para renderizar los usuarios
})

userForm.addEventListener('submit', async e=> {
    e.preventDefault() //evita que se recargue la pagina al enviar el formulario
    
    const nombre = userForm['nombre'].value //el value es para obtener el valor del input
    const apellido = userForm['apellido'].value
    const correo = userForm['correo'].value
    const nacimiento = userForm['nacimiento'].value
    const password = userForm['password'].value

    const response = await fetch('/dato/api', { //ruta a la que se enviaran los datos
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' //tipo de contenido que se enviara
        },
        body: JSON.stringify({ //convierte el objeto a una cadena JSON
            nombre,
            apellido,
            correo,
            nacimiento,
            password
            
        })
    })

    const data = await response.json()
    console.log(data)

    userForm.reset() //resetea el formulario despues de enviarlo
})
