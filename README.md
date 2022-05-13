# Dundle-bee-pancake
This repository is part of a bigger project that is focused on controling products inside a supermarket and it's flow  from the store entrance to the checkout. In this repo we are going to take care of messagery with RabbitMQ microsservice, the agents to connect into the database and the database itself. 


## Database
The database consists in a 4 table model indentified on the example image below. The university project was designed to have only one stock, one shelve, and N products.

![alt text](https://github.com/rgazoni/Dundle-bee-pancake/blob/media/DatabaseImages/DatabaseModel.png)

Each product have its respective ID, quantity, due date, fabrication date, lot and origin meanwhile the stock and the shelve will store the products quantity storaged on itself. Each product owns a category with a name, as an example "Coke".

The database has 3 procedures that are in charge of doing the supermarket transactions wich are:
- Add product to the storage
- Move produt from the storage to the shelve
- Remove product from the shell (Simulating the sale act, we are not considering product prices)

To do so we used MariaDB an open source relational database base.

## Agents
The agents are responsible by the communication between the message broker app and the Database they call the select commands and the procedures recieving and sending information troughth the RabbitMQ communicating with the other app interfaces. 