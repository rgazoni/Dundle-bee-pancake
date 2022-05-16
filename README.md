# Dundle-bee-pancake

This repository is part of a bigger project that is focused on controling products inside a supermarket and it's flow  from the store entrance to the checkout. In this repo we are going to take care of messagery with RabbitMQ microsservice, the agents to connect into the database and the database itself. 


# Arquitetura do sistema

A imagem abaixo descreve a arquitetura do sistema.

<br>

<img src="resources/images/Redes.png" style="margin-left: auto; margin-right: auto; width: 70%; display: block;">

<br>

Temos no frontend um sistema Web, um aplicativo e o Kibana. Já no backend temos a API, a mensageria, os agentes e o banco de dados. 
Iremos focar mais no que foi desenvolvido nesse repositório, que é o sistema do backend e a elastic stack. Temos uma api que coleta informações vindo de rotas 