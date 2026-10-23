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
    raise SystemExit("Contract not found. Deploy the contract again.")

abi = json.loads(
    (BUILD / "FlightDelayInsurance.abi.json").read_text()
)

contract = web3.eth.contract(address=address, abi=abi)
accounts = web3.eth.accounts

if len(accounts) < 3:
    raise SystemExit("At least three accounts are required.")

customer = accounts[2]
flight_number = "EI904"

# Use the blockchain time and schedule departure one hour ahead.
scheduled_departure = web3.eth.get_block("latest")["timestamp"] + 3600
premium = contract.functions.PREMIUM().call()
compensation = contract.functions.COMPENSATION().call()

balance_before = contract.functions.getContractBalance().call()
reserved_before = contract.functions.reservedFunds().call()
count_before = contract.functions.policyCount().call()

print("Purchasing policy...")

transaction_hash = contract.functions.buyPolicy(
    flight_number,
    scheduled_departure,
).transact({
    "from": customer,
    "value": premium,
})

receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

if receipt["status"] != 1:
    raise SystemExit("Policy purchase failed.")

events = contract.events.PolicyPurchased().process_receipt(receipt)

if len(events) != 1:
    raise SystemExit("Expected one PolicyPurchased event.")

policy_id = events[0]["args"]["policyId"]
policy = contract.functions.policies(policy_id).call()

balance_after = contract.functions.getContractBalance().call()
reserved_after = contract.functions.reservedFunds().call()

if (
    policy[0] != customer
    or policy[2]
    or contract.functions.policyCount().call() != count_before + 1
    or balance_after != balance_before + premium
    or reserved_after != reserved_before + compensation
):
    raise SystemExit("Unexpected policy or balance results.")

purchase = {
    "contract_address": address,
    "policy_id": policy_id,
    "customer": customer,
    "flight_number": flight_number,
    "scheduled_departure": scheduled_departure,
    "flight_id": web3.to_hex(policy[1]),
}

(BUILD / "purchase.json").write_text(
    json.dumps(purchase, indent=2) + "\n"
)

print("Policy purchased successfully")
print("Transaction:", web3.to_hex(transaction_hash))
print("Policy ID:", policy_id)
print("Customer:", customer)
print("Flight ID:", purchase["flight_id"])
print("Scheduled departure:", scheduled_departure)
print("Paid:", policy[2])
print("Contract balance:", web3.from_wei(balance_after, "ether"), "ETH")
print("Reserved funds:", web3.from_wei(reserved_after, "ether"), "ETH")
print("Purchase saved to build/purchase.json")