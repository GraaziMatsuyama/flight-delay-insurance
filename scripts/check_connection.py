from web3 import Web3

RPC_URL = "http://127.0.0.1:8545"


def main():
    web3 = Web3(Web3.HTTPProvider(RPC_URL))

    if not web3.is_connected():
        raise SystemExit("Connection failed. Check that Ganache is running.")

    accounts = web3.eth.accounts

    print("Connected to Ganache")
    print("Chain ID:", web3.eth.chain_id)
    print("Available accounts:", len(accounts))

    if len(accounts) < 3:
        raise SystemExit("At least three accounts are required.")

    print("Insurer:", accounts[0])
    print("Reporter:", accounts[1])
    print("Customer:", accounts[2])


if __name__ == "__main__":
    main()