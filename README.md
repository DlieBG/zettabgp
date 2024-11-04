```
888888888888                                           88888888ba     ,ad8888ba,   88888888ba   
         ,88               ,d       ,d                 88      "8b   d8"'    `"8b  88      "8b  
       ,88"                88       88                 88      ,8P  d8'            88      ,8P  
     ,88"     ,adPPYba,  MM88MMM  MM88MMM  ,adPPYYba,  88aaaaaa8P'  88             88aaaaaa8P'  
   ,88"      a8P_____88    88       88     ""     `Y8  88""""""8b,  88      88888  88""""""'    
 ,88"        8PP"""""""    88       88     ,adPPPPP88  88      `8b  Y8,        88  88           
88"          "8b,   ,aa    88,      88,    88,    ,88  88      a8P   Y8a.    .a88  88           
888888888888  `"Ybbd8"'    "Y888    "Y888  `"8bbdP"Y8  88888888P"     `"Y88888P"   88           
```

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

### Environment Variables
The following environment variables can be used to specify connection parameters.
```
RABBIT_MQ_HOST
MONGO_DB_HOST
MONGO_DB_PORT
```

## Usage
ZettaBGP provides a CLI interface with some commands for testbed simulations as well for production use.

### Comands
#### `zettabgp exabgp`
The `exabgp` subcommand is used for processing ExaBGP Messages.\
The process can be started from within ExaBGP.\
The Messages will be received using the stdin pipe.
```
Options:
  -r, --no-rabbitmq
  -l, --no-mongodb-log
  -s, --no-mongodb-state
  -t, --no-mongodb-statistics
```

#### `zettabgp mrt-simulation`
The `mrt-simulation` subcommand is used for processing MRT files.\
It is mendatory to provide a valid path to a mrt file.\
```
Arguments:
  MRT_FILE

Options:
  -r, --no-rabbitmq
  -l, --no-mongodb-log
  -s, --no-mongodb-state
  -t, --no-mongodb-statistics
```

## Debugging
Some sample json messages for debugging purposes from ExaBGP can be found in the `samples` directory.

### Remote Port Forward
When you want to access the MongoDB and RabbitMQ instances on the testbed, you can use a remote port forward with ssh to forward the application ports to your local machine.
```
ssh -L 15672:127.0.0.1:15672 -L 5672:127.0.0.1:5672 -L 27017:127.0.0.1:27017 node103
```

## Models
```python
class ChangeType(Enum):
    ANNOUNCE = 1,
    WITHDRAW = 2,

class NLRI(BaseModel):
    prefix: str
    length: int

class OriginType(Enum):
    IGP = 1
    EGP = 2
    INCOMPLETE = 3

class AsPathType(Enum):
    AS_SET = 1
    AS_SEQUENCE = 2
    AS_CONFED_SET = 3
    AS_CONFED_SEQUENCE = 4

class AsPath(BaseModel):
    type: AsPathType
    value: list[int]

class Aggregator(BaseModel):
    router_id: str
    router_as: int

class PathAttributes(BaseModel):
    origin: Optional[OriginType] = None
    as_path: Optional[list[AsPath]] = None
    next_hop: Optional[list[str]] = None
    multi_exit_disc: Optional[int] = None
    local_pref: Optional[int] = None
    atomic_aggregate: Optional[bool] = None
    aggregator: Optional[Aggregator] = None
    community: Optional[list[list[int]]] = None
    large_community: Optional[list[list[int]]] = None
    extended_community: Optional[list[int]] = None
    orginator_id: Optional[str] = None
    cluster_list: Optional[list[str]] = None

class RouteUpdate(BaseModel):
    timestamp: datetime = datetime.now()
    peer_ip: str
    local_ip: str
    peer_as: int
    local_as: int
    path_attributes: PathAttributes
    change_type: ChangeType = None
    nlri: NLRI = None
```
