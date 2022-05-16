## Agents
The agents are responsible by the communication between the message broker app and the Database they call the select commands and the procedures recieving and sending information troughth the RabbitMQ communicating with the other app interfaces. 

We are using three differents agents to communicate with the database using the RabbitMQ as a message broker.

The agents are:
- shelves
- stock
- stock_shelves

The agents connect with the database using the connect function.

### Stock Agent
The Stock agent can add products at the stock and query all products storaged in the stock.

### Shelves Agent
The Shelves agent moves query the item name on the shelve, simulates the act of sale and query all prodcts on the shelves. 

### Stock_Shelves Agent
The Stock Shelves agent moves the products between the stock and the shelve.