import json
from pathlib import Path

from web3 import Web3

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not web3.is_connected():
    raise SystemExit("Connection failed. Start Ganache first.")

if web3.eth.chain_id != 1337:
    raise SystemExit("Expected the local Ganache network (1337).")

accounts = web3.eth.accounts

if len(accounts) < 3:
    raise SystemExit("At least three accounts are required.")

insurer = accounts[0]
reporter = accounts[1]

abi = json.loads(
    (BUILD / "FlightDelayInsurance.abi.json").read_text()
)

bytecode = (
    BUILD / "FlightDelayInsurance.bytecode.txt"
).read_text().strip()

if not bytecode.startswith("0x"):
    bytecode = "0x" + bytecode

contract = web3.eth.contract(abi=abi, bytecode=bytecode)

print("Deploying FlightDelayInsurance...")

transaction_hash = contract.constructor(reporter).transact({
    "from": insurer
})

receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

if receipt["status"] != 1 or not receipt["contractAddress"]:
    raise SystemExit("Contract deployment failed.")

address = receipt["contractAddress"]
deployed = web3.eth.contract(address=address, abi=abi)

if deployed.functions.insurer().call() != insurer:
    raise SystemExit("Unexpected insurer address.")

if deployed.functions.reporter().call() != reporter:
    raise SystemExit("Unexpected reporter address.")

deployment = {
    "chain_id": web3.eth.chain_id,
    "contract_address": address,
    "transaction_hash": web3.to_hex(transaction_hash),
    "insurer": insurer,
    "reporter": reporter,
}

(BUILD / "deployment.json").write_text(
    json.dumps(deployment, indent=2) + "\n"
)

print("Contract deployed:", address)
print("Transaction:", web3.to_hex(transaction_hash))
print("Insurer:", insurer)
print("Reporter:", reporter)
print("Contract balance:", deployed.functions.getContractBalance().call())
print("Deployment saved to build/deployment.json")