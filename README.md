
<h1 style="text-align:center"> API Menú digital </h1> 

<strong><h2 style="text-align:center">Descripción</h2></strong>
<h4>API desarrollada para un menú digital donde el cliente del comercio puede ver los productos junto con la descripción y precios de los mismos. El proyecto está dividido en 2 partes: <br><br>

- API <br>

- Aplicación de escritorio. <br><br>

En este repositorio solo habrá información de la API. Para la app de escritorio, debes entrar al siguiente repositorio
<a href="https://github.com/ThomySjs/App_productos">App productos</a>.
</h4>

<strong><h2 style="text-align:center">Pequeña historia</h2></strong>
<h4>La idea para este proyecto surgió como solución a un problema que ocurría muy seguido en mi trabajo (una heladería) donde, además de ofrecer el producto principal, también contábamos con una carta de cafetería. Al llenarse el local nos quedábamos sin cartas, por lo que se me ocurrió una forma de no depender de las mismas: &quot;Un menú digital&quot;. <br><br> 
La primera versión del proyecto era simplemente el menú donde el cliente podía entrar para ver los productos y sus precios. Si bien ese era un buen enfoque, rápidamente me surgió la duda: ¿Qué pasa cuando cambian los precios o en caso de tener que modificar un producto? Por lo que decidí desarrollarlo con la posibilidad de que el empleado pueda editar el menú a conveniencia.
</h4>

<strong><h2 style="text-align:center">Tecnologías y división</h2></strong>
<strong>Tecnologías utilizadas: 
<ol>
    <li>Python</li>
    <li>Flask</li>
    <li>Flask-mail</li>
    <li>SQLite3, SQLAlchemy y Alembic para bases de datos.</li>
    <li>JWT, Bcrypt e Itsdangerous para seguridad.</li>
</ol>
</strong> <br>
<strong>Base de datos: <br></strong>
Decidí utilizar SQLite3 ya que el proyecto está pensado para un local chico que no maneja gran cantidad de datos, por lo que algo simple y ligero es la mejor opción. Para las migraciones implementé Alembic. <br><br>
<strong>Seguridad: <br></strong>

El proyecto cuenta con un sistema de registro y logueo con verificación vía mail utilizando Flask-mail. El registro tiene una clave única necesaria para crear la cuenta. <br>
Los endpoints cuyo propósito es realizar operaciones CRUD están protegidos por JWT, es decir, para realizar dichas operaciones es necesario estar registrado. Además, utilicé Bcrypt para evitar guardar las contraseñas como texto plano.<br>

<strong>Escalabilidad: <br></strong>
La estructura está bien organizada y utiliza blueprints, permitiendo agregar nuevas funcionalidades sin necesidad de reescribir o modificar código ya existente.

---
<strong><h2 style="text-align:center"> Funcionalidades</h2></strong>

<h3 style="text-align:center"><strong>Página principal.</strong></h3>

<h3><strong>Menú</strong></h3>
<h4>
Retorna un template que utiliza los datos recopilados para mostrarlos en el menú. <br><br>
Método : GET <br>
URL : /Menu <br>
Variables del template:<br>

- data (Lista de tuplas con información de los productos)
- base_template (El template que retorna el endpoint extiende el template base, por lo que deberías pasar esa base en esta variable)<br><br>


> Nota: Este es el único endpoint al que debería poder acceder el cliente del comercio.

</h4>

<h3 style="text-align:center"><strong>Inicio de sesión y validaciones.</strong></h3>

<h3><strong>Registro</strong></h3>
<h4>

Método : POST <br>
URL : /register <br>
Content-type : application / JSON<br>
Ejemplo de petición: <br><br>
{<br>
    &emsp;`name` : "yourname",<br>
    &emsp;`mail`: "example@gmail.com",<br>
    &emsp;`password`: "supersecretpassword",<br>
    &emsp;`key`: "supersecretkey"<br>
}
</h4>

<h3><strong>Log in</strong></h3>
<h4>

Método : POST <br>
URL : /login <br>
Content-type : application / JSON<br>
Ejemplo de petición: <br><br>
{<br>
    &emsp;`mail`: "example@gmail.com",<br>
    &emsp;`password`: "supersecretpassword",<br>
}
</h4>
</h4>

<h3><strong>Refresh token</strong></h3>
<h4>

Método : POST <br>
URL : /refresh <br>
Content-type : application / JSON<br>
Protección : JWT refresh token.
</h4>

---
<h3 style="text-align:center"><strong>Operaciones CRUD con productos.</strong></h3>

<h3><strong>Obtener productos</strong></h3>
<h4>

Método : POST <br>
URL : /products <br>
Content-type : application / JSON<br>
Protección : JWT. <br>
Ejemplo de petición: <br><br>
{<br>
    &emsp;`order`: "price"<br>
}<br>
>Nota: Este endpoint también podría utilizar un método GET y pasar por parámetro en la URL el orden con el que solicita los productos. Simplemente decidí darle otro enfoque pasando el orden a través de un JSON.
</h4>

<h3><strong>Obtener producto por ID</strong></h3>
<h4>

Método : GET <br>
URL : /products/<int:id> <br>
Protección : JWT. <br>
</h4>

<h3><strong>Agregar producto</strong></h3>
<h4>

Método : POST <br>
URL : /products/add <br>
Content-type : application / JSON<br>
Protección : JWT. <br>
Ejemplo de petición: <br><br>
{<br>
    &emsp;`product_name`: productname,<br>
    &emsp;`price`: 1500.0,<br>
    &emsp;`description`: somedescription,<br>
    &emsp;`category`: somecategory,<br>
    &emsp;`available`: False<br>
}<br><br>
</h4>

<h3><strong>Actualizar producto</strong></h3>
<h4>

Método : PUT <br>
URL : /products/update <br>
Content-type : application / JSON<br>
Protección : JWT. <br>
Ejemplo de petición: <br><br>
{<br>
    &emsp;`product_id`: 0,<br>
    &emsp;`product_name`: productname,<br>
    &emsp;`price`: 1500.0,<br>
    &emsp;`description`: somedescription,<br>
    &emsp;`category`: somecategory,<br>
    &emsp;`available`: True<br>
}<br><br>
</h4>

<h3><strong>Eliminar producto</strong></h3>
<h4>

Método : DELETE <br>
URL : /products/delete <br>
Content-type : application / JSON<br>
Protección : JWT. <br>
Ejemplo de petición: <br><br>
{<br>
    &emsp;`product_id`: 0,<br>
}<br><br>
</h4>

<h3><strong>Obtener historial de cambios</strong></h3>
<h4>

Método : GET <br>
URL : /products/changelog <br>
Protección : JWT. <br>
</h4><br>

> Para más información sobre los distintos endpoints, puedes revisar la documentación dentro del código. 

---


<strong><h2 style="text-align:center">Cómo probar la API</h2></strong>

<strong><h3>Activar en servidor local</h3></strong>
<h4>
Una vez que hayas clonado el proyecto, dentro de la carpeta principal debes crear un entorno virtual.<br><br>
<code>python3 -m venv env</code><br><br>
<code>venv\scriptsctivate</code><br><br>
Con el entorno virtual creado y activado, ejecuta el siguiente comando para instalar todas las dependencias necesarias.<br><br>
<code>pip install -r requirements.txt</code><br><br>
Con todo ya instalado solo queda configurar las variables de entorno (puedes crear un archivo .env). <br>Ejemplo de cuáles son las variables necesarias. <br><br>

`SECRET_KEY` = 'yoursupersecretkey'<br>
`SECURITY_SALT` = 'somesalt'<br>
`SQLALCHEMY_DATABASE_URI` = 'sqlite:///example.sqlite3'<br>
`REGISTRATION_KEY` = 'supersecretregkey' (La clave única de la que hablé más arriba)<br><br>

`MAIL_SERVER` = 'smtp.gmail.com' <br>
`MAIL_PORT` = 587 <br>
`MAIL_USE_SSL` = True <br>
`MAIL_USE_TLS` = True <br>
`MAIL_USERNAME` = 'youremail@gmail.com' <br>
`MAIL_PASSWORD` = 'yourpassword' (Debes habilitar la contraseña de aplicación) <br>
`MAIL_DEFAULT_SENDER` = 'youremail@gmail.com' <br>

Por último, queda iniciar la app con el siguiente comando<br><br>
<code>python3 run.py</code><br>

Si todo salió bien, deberías ver este mensaje en tu línea de comandos<br>
</h4>
<img src="staticReadme/flask.jpg"></img>

<strong><h3> Probar con Postman</h3></strong>

<h4>
Primero debemos registrarnos y validar el mail. <br><br>
<img src="staticReadme/register.jpg">
<img src="staticReadme/created.jpg"> <br><br>

Una vez registrados, debemos iniciar sesión y recibiremos el código de acceso como respuesta (además de un refresh token para mantener la sesión). <br><br>
<img src="staticReadme/login.jpg">
<img src="staticReadme/access.jpg"><br><br>

Accedemos a un endpoint protegido sin el token de acceso para comprobar. <br><br>
<img src="staticReadme/Unauthorized.jpg"><br><br>

Agregamos el token de acceso al encabezado y hacemos la misma petición. <br><br>
<img src="staticReadme/Authorization.jpg">
<img src="staticReadme/created.jpg"><br><br>

Puedes seguir probando con los distintos endpoints. Recuerda agregar el token de acceso para las peticiones y nunca compartas las claves secretas de la aplicación.
</h4>
