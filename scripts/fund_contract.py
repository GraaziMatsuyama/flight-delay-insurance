import json
from pathlib import Path

from web3 import Web3

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not web3.is_connected():
    raise SystemExit("Connection failed. Start Ganache first.")

deployment = json.loads((BUILD / "deployment.json").read_text())

if web3.eth.chain_id != deployment["chain_id"]:
    raise SystemExit("Network does not match the deployment.")

address = deployment["contract_address"]

if not web3.eth.get_code(address):
    raise SystemExit("Contract not found. Run deploy_contract.py again.")

abi = json.loads(
    (BUILD / "FlightDelayInsurance.abi.json").read_text()
)

contract = web3.eth.contract(address=address, abi=abi)
insurer = contract.functions.insurer().call()

balance_before = contract.functions.getContractBalance().call()
amount = web3.to_wei(1, "ether")

print("Funding contract with 1 test ETH...")

transaction_hash = contract.functions.fundContract().transact({
    "from": insurer,
    "value": amount,
})

receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

if receipt["status"] != 1:
    raise SystemExit("Funding failed.")

balance_after = contract.functions.getContractBalance().call()

if balance_after != balance_before + amount:
    raise SystemExit("Unexpected contract balance.")

print("Funding successful")
print("Transaction:", web3.to_hex(transaction_hash))
print("Balance before:", web3.from_wei(balance_before, "ether"), "ETH")
print("Balance after:", web3.from_wei(balance_after, "ether"), "ETH")