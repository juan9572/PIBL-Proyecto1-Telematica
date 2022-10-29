# PIBL-Proyecto1-Telematica

## Introduccion

En este repositorio se encuentra alojado el proxy inverso desarrollado para
la materia de Telematica en el semestre 2022-2. En este documento vamos a dar
una breve introduccion a lo que fue todo el desarrollo, las conclusiones que
se generaron a lo largo de la practica y las referencias teoricas sobre las
cuales construimos este proyecto.
## Desarrollo

En terminos tecnicos, el proxy fue construido sobre python 3, haciendo uso de
las librerias *socket* (para el manejo de la API Socket), *time* (para el manejo
de los recursos almacenados en el cache) y *threading* (para el manejo de los
hilos).


### Configuracion del proxy

Para la parametrizacion del proxy, decidimos usar un archivo .config en la
carpeta raiz del proyecto. La configuracion seria tal que asi.

~~~
HOST=127.0.0.1
PUERTO=8080
SERVERS=54.89.232.250:8080, 18.212.172.147:8080, 3.89.24.54:8080
BUFF_SIZE=8192
TTL=1
~~~

Host: se refiere a la ip privada en donde el proxy va a estar corriendo.
Puerto: Se refiere al puerto que se dispone en la maquina para que el proxy
escuche peticiones.
Servers: En este apartado se espera que el usuario ingrese los servidores a los
cuales el proxy va a redirigir de la sigueinte manera
~~~
<SERVER_IP>:<SERVER_PORT>, <SERVER2_IP>:<SERVER2_PORT>...
~~~
Buff_size: Es el tamaño del buffer que se va a esperar a la hora de mandar
y recibir peticiones.
TTL: O time to live, es el tiempo maximo que una entrada permanecera en el
cache. El tiempo esta en minutos.

### Balanceador de carga

La tecnica para balancear carga que usamos fue *Round Robin* que dentro del
codigo la implementamos como una operacion ternaria que nos devuelve el numero
del servidor al cual vamos a redirigir una request especifica.

### Cache

Para el cache usamos un archivo *.txt* que almacena una relacion Request - Response
que despues usamos para construir un diccionario dentro del codigo. Sobre este
diccionario realizamos busquedas en las key para ver si una request entrante
existe dentro del diccionario y asi evitarnos redirigir la peticion y esperar la
respuesta del servidor. Cada entry dentro del archivo se borrara despues de haber
pasado determinado tiempo que el usuario debe parametrizar en el archivo *.config*

### Log

Cada que se recibe una peticion o se manda un response, el proxy imprimira por
consola y en un archivo de texto toda la informacion. De tal manera que se le
ofrezca al usuario una fuente de trazabilidad en caso de que algo no vaya como
es esperado.

### Proxy inverso

El funcionamiento del codigo es de la siguiente forma, usamos *sockets* para
escuchar en el puerto parametrizado las request de los clientes, una vez se
establezca la conexion creamos un hilo de manera tal que podamos soportar
peticiones concurrentes. Cuando la conexion con el cliente es establecida
recibimos la request y la analizamos, si esa request se encuentra en el cache
no realizamos ningun redireccionamiento al server puesto que ya sabemos cual es
el response que hay que enviar, si no se encuentra en el cache usamos el round
robin para redirigir la peticion a uno de los servidores parametrizados. Una
vez el server proceses la peticion y nos devuelva el response almacenamos esa
request y ese response en el cache (que dentro del codigo representamos como un
diccionario) luego le enviamos la response al cliente y quedamos atentos a
posteriores peticiones. Asi se quedara el programa funcionando infinitamente
hasta que el usuario mande un QUIT que es donde se finaliza la conexion con ese
cliente y se cierra el hilo.
### Justificacion del uso de Python

Elegimos Python por encima de cualquier otro lenguaje simplemente porque
consideramos que es un lenguaje muy potente a la hora de manejar la grandes
porciones de informacion, que es justamente lo que necesitamos en el momento
de desarrollar un cache eficiente y que funcione perfectamente.

Como se menciono anteriormente a la hora de guardar el cache estamos
almacenando en un diccionario toda la cadena de bytes de la respuesta del
servidor de una forma integra, por tal motivo un lenguaje que permita realizar
esto es una parte fundamental. De igual manera, para almacenar esa cadena de
en un archivo de texto era necesario parsear el dato a string cosa que python
maneja sin problemas.

## Conclusiones

En conclusion podemos decir que el desarrollo de la practica fue cuanto
menos interante. Muchas de las cosas habladas en clase fueron llevadas a la
practica lo cual solidifica los conocimientos obtenidos y ademas permite darle
una vista muy especial a como funcionan las cosas en el mundo real.

Creemos que este tipo de practicas, donde desarrollamos conceptos de forma
practica funcionan demasiado bien para personas en proceso de aprendizaje como
nosotros.
## Referencias

> https://www.f5.com/es_es/services/resources/glossary/reverse-proxy
