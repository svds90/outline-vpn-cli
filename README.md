# outline-vpn-cli
**outline-vpn-cli**: a dockerized command-line tool for interacting with the Outline VPN API via HTTP requests, designed for managing server configuration and client access keys.

Requires [docker](https://www.docker.com/)

## Example

```
~ outline get --server srv04
=================  =====================================================
key                https://123.123.123.123:12345/yVeRSGYQkrJHgja849aFOxw
name               ebalrkn
id                 b8e8anio-cc85-483a-12f2-c9461uv01k33
metric_status      False
created_time       19 August 2022, 09:16:33 PM
version            1.8.1
data_limit
port_for_new_keys  51830
hostname_for_keys  123.123.123.123
=================  =====================================================

~ outline get -s srv04 --keys --metrics
====  ==================
  ID    Transferred data
====  ==================
   2              134.96
   3              136.05
   4               50.42
   5               62.72
   7               76.18
====  ==================

~ outline json --list
=======  =====================================================
srv01    https://123.123.123.123:12345/yVeRSGYQkrJHgja849aFOxw
srv02    https://13.13.13.13:12345/yVeRSGYQkUXcLjja849axw
srv03    https://18.188.167.34:5778/yVeRSGYQkrJHgja849aFOxw
=======  =====================================================
```


## Installation

### auto

```bash
curl -sSL https://raw.githubusercontent.com/svds90/outline-vpn-cli/master/setup.sh | sudo bash
```
### manually
pull image
```
docker pull svds90/outline-vpn-cli:latest
```
create container
```
docker run -dit --restart always --name outline-vpn-cli svds90/outline-vpn-cli
```
for ease of use, you can create an alias:
```
alias outline='docker exec outline-vpn-cli python main.py' >> ~/path/to/aliases or bashrc/zshrc
```

### or 

script, for instance, in the **/usr/local/bin** (or any other directory with scripts) directory with a name of your choice, such as 'outline'.
```
echo 'docker exec outline-vpn-cli python main.py "\$@"' > /usr/local/bin/outline
```

## Usage

You can use abbreviated options instead of flags, refer to --help for details.

- [outline-vpn-cli](#outline-vpn-cli)
  - [Example](#example)
  - [Installation](#installation)
    - [auto](#auto)
    - [manually](#manually)
    - [or](#or)
  - [Usage](#usage)
    - [JSON command](#json-command)
    - [GET command](#get-command)
    - [SET command](#set-command)
    - [ADD command](#add-command)
    - [DEL command](#del-command)

___

### JSON command

For ease of use, it is recommended to add servers to servers.json, which is stored inside the container, for example:

```
outline json --add server1 https://123.123.123.123:12345/yVeRSGYQkrJHgja849aFOxw
```

lists servers:
```
outline json --list
```

removes server:
```
outline json --remove server2
```

get API url:
```
outline json --get-url server1
```

rename server:
```
outline json --name server1 server_new
```
_____
### GET command

get server info:
```
outline get --server server_new
```

lists all keys:
```
outline get --server server_new --keys
```

get key by id:
```
outline get --server server_new --key 2
```

returns the data transferred per access key:
```
outline get --server server_new --keys --metrics
```

get telemetry status:
```
outline get --server server_new --telemetry
```

retrieve transferred data by key ID:
```
outline get --server server_new --key 2 --metrics
```
____
### SET command

changes hostname:
```
outline set --server server_new --hostname new_hostname
```

renames server:
```
outline set --server server_new --name new_name
```

changes port for new keys:
```
outline set --server server_new --port 12345
```

rename key:
```
outline set --server server_new --rename-key 5 new_name
```

sets a data limit for the given access key (bytes):
```
outline set --server server_new --key-data-limit 5 100000
```

for disabling data limit:
```
outline set --server server_new --key-data-limit 5 off
```

sets a data transfer limit for all access keys (bytes):
```
outline set --server server_new --global-limit 100000000
```

for disabling global data limit:
```
outline set --server server_new --global-limit off
```

____

### ADD command

creates a new access key:
```
outline add --server server_new --new-key
```

____

### DEL command

removes key:
```
outline --server server_new --remove-key 3
```