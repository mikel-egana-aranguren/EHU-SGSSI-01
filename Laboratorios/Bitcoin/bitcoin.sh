docker run -d --name bitcoind-regtest ruimarinho/bitcoin-core -regtest=1 -server=1 -fallbackfee=0.0002
alias bitcoin-cli="docker exec -u bitcoin bitcoind-regtest bitcoin-cli -regtest"
bitcoin-cli getblockchaininfo