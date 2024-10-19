# ZettaBGP
...

## Setup
### ExaBGP
A valid ExaBGP configuration must be provided that includes a process for ZettaBGP with the `json` encoder.\
You can use this reference as a sample.
```
neighbor 172.17.179.104 {
	router-id 172.17.179.103;
	local-address 172.17.179.103;
	local-as 1;
	peer-as 1;
	hold-time 180;

	api {
		processes [zettabgp];
		receive {
			parsed;
			update;
		}
	}
}

process zettabgp {
	run python3 /home/imprj/zettabgp/src/main.py;
	encoder json;
}
```

### Database and Message Queue
A sample setup for MongoDB and RabbitMQ is provided in the `db` directory.\
To run the docker compose setup run the following command in that directory.\
```
sudo docker compose up -d
```
The data will be stored in the `data` directory.

## Expected Functionality
### RabbitMQ Adapter
The RabbitMQ Adapter handles incoming `announce` and `withdraw` messages and forwards them to the `zettabgp` exchange.\
For testing purposes the queues `test_bgp_updates`, `test_bgp_announces` and `test_bgp_withdraws` are bind to the exchange.

## Debugging
Some sample json messages for debugging purposes from ExaBGP can be found in the `samples` directory.
