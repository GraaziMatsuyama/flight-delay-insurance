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
policy_id = purchase["policy_id"]
policy = contract.functions.policies(policy_id).call()

customer = policy[0]

if customer != purchase["customer"]:
    raise SystemExit("Unexpected policy owner.")

if policy[2]:
    raise SystemExit("Compensation already paid.")

compensation = contract.functions.COMPENSATION().call()
balance_before = contract.functions.getContractBalance().call()
reserved_before = contract.functions.reservedFunds().call()
customer_before = web3.eth.get_balance(customer)

print("Claiming compensation...")

transaction_hash = contract.functions.claimCompensation(
    policy_id
).transact({"from": customer})

receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

if receipt["status"] != 1:
    raise SystemExit("Compensation claim failed.")

updated_policy = contract.functions.policies(policy_id).call()
balance_after = contract.functions.getContractBalance().call()
reserved_after = contract.functions.reservedFunds().call()
customer_after = web3.eth.get_balance(customer)

gas_cost = receipt["gasUsed"] * receipt["effectiveGasPrice"]

if (
    not updated_policy[2]
    or balance_after != balance_before - compensation
    or reserved_after != reserved_before - compensation
    or customer_after != customer_before + compensation - gas_cost
):
    raise SystemExit("Unexpected payment or balance results.")

print("Compensation paid successfully")
print("Transaction:", web3.to_hex(transaction_hash))
print("Policy ID:", policy_id)
print("Customer:", customer)
print("Compensation:", web3.from_wei(compensation, "ether"), "ETH")
print("Paid:", updated_policy[2])
print("Contract balance:", web3.from_wei(balance_after, "ether"), "ETH")
print("Reserved funds:", web3.from_wei(reserved_after, "ether"), "ETH")
print("Customer balance verified, including transaction gas")