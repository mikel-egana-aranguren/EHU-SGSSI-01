#!/bin/bash

# containers
docker run -d --name bitcoind-regtest ruimarinho/bitcoin-core -regtest=1 -server=1 -fallbackfee=0.0002
alias bitcoin-cli="docker exec -u bitcoin bitcoind-regtest bitcoin-cli -regtest"
bitcoin-cli getblockchaininfo

# docker compose
docker compose up
alias bitcoin-cli="docker exec -u bitcoin bitcoind-explorer bitcoin-cli -regtest -rpcuser=labw -rpcpassword=labw"
bitcoin-cli getblockchaininfo