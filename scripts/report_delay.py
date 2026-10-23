import json
from pathlib import Path

from web3 import Web3

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not web3.is_connected():
    raise SystemExit("Connection failed. Start Ganache first.")

deployment = json.loads((BUILD / "deployment.json").read_text())
purchase = json.loads((BUILD / "purchase.json").read_text())

if web3.eth.chain_id != deployment["chain_id"]:
    raise SystemExit("Network does not match the deployment.")

address = deployment["contract_address"]

if purchase["contract_address"] != address:
    raise SystemExit("Purchase belongs to a different contract.")

if not web3.eth.get_code(address):
    raise SystemExit("Contract not found. Deploy the contract again.")

abi = json.loads(
    (BUILD / "FlightDelayInsurance.abi.json").read_text()
)

contract = web3.eth.contract(address=address, abi=abi)
flight_id = web3.to_bytes(hexstr=purchase["flight_id"])
reporter = contract.functions.reporter().call()

flight = contract.functions.flights(flight_id).call()

if flight[0] == 0:
    raise SystemExit("Flight not found.")

if flight[2]:
    raise SystemExit("Delay already reported.")

# Advance local test-chain time past departure.
current_time = web3.eth.get_block("latest")["timestamp"]
seconds_to_advance = max(0, flight[0] - current_time + 1)

if seconds_to_advance > 0:
    response = web3.provider.make_request(
        "evm_increaseTime", [seconds_to_advance]
    )
    if "error" in response:
        raise SystemExit(str(response["error"]))

    response = web3.provider.make_request("evm_mine", [])
    if "error" in response:
        raise SystemExit(str(response["error"]))

if web3.eth.get_block("latest")["timestamp"] < flight[0]:
    raise SystemExit("Blockchain time is still before departure.")

balance_before = contract.functions.getContractBalance().call()
reserved_before = contract.functions.reservedFunds().call()

print("Reporting a simulated delay of 120 minutes...")

transaction_hash = contract.functions.reportDelay(
    flight_id, 120
).transact({"from": reporter})

receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

if receipt["status"] != 1:
    raise SystemExit("Delay reporting failed.")

updated_flight = contract.functions.flights(flight_id).call()
balance_after = contract.functions.getContractBalance().call()
reserved_after = contract.functions.reservedFunds().call()

if (
    updated_flight[1] != 120
    or not updated_flight[2]
    or balance_after != balance_before
    or reserved_after != reserved_before
):
    raise SystemExit("Unexpected flight or balance results.")

print("Delay reported successfully")
print("Transaction:", web3.to_hex(transaction_hash))
print("Reporter:", reporter)
print("Delay minutes:", updated_flight[1])
print("Reported:", updated_flight[2])
print("Contract balance:", web3.from_wei(balance_after, "ether"), "ETH")
print("Reserved funds:", web3.from_wei(reserved_after, "ether"), "ETH")