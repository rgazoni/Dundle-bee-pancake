# RabbitMQ

<b>Foi estruturado o sistema de mensageria - RabbitMQ, atráves do paradigma de programação de orientação à objetos.</b>  
<br>

## Arquitetura do sistema de mensageria

## RabbitSetup.py

Nessa módulo temos a classe pai do sistema, no qual é responsável por criar uma conexão com com o sistema de mensageria, sendo ele um Subscriber ou um Publisher. Além disso, declaramos todas as filas do sistema e suas respectivas routing keys - a estrutura segue a arquitetura mostrada acima. Também é interessante notar que utilizamos um direct exchange nativo do protocolo utilizado pelo RabbitMQ amqp.direct. 
