## Python and Ganache integration tests

### Environment
- Ganache 7.9.2
- Local RPC: http://127.0.0.1:8545
- Chain ID: 1337
- EVM target: Shanghai
- Python 3.14.6
- web3.py 8.0.0
- Simulated flight information and test ETH

### Account roles
- Ganache account 0: insurer
- Ganache account 1: authorised reporter
- Ganache account 2: customer

### Completed workflow

| Step | Expected result | Observed result | Status |
| --- | --- | --- | --- |
| Connect to Ganache | Connection established, chain ID 1337 and 10 accounts | Connection established, chain ID 1337 and 10 accounts | Passed |
| Deploy contract | Insurer and reporter stored correctly; initial balance 0 ETH | Roles verified; balance 0 ETH | Passed |
| Fund contract | Insurer adds 1 ETH | Balance increased to 1 ETH | Passed |
| Purchase policy | Customer pays 0.01 ETH; 0.05 ETH reserved | Policy 1 created; balance 1.01 ETH; reserves 0.05 ETH | Passed |
| Report delay | Authorised reporter records 120 minutes after departure | Delay 120; reported true; reserves remained 0.05 ETH | Passed |
| Claim compensation | Customer receives 0.05 ETH; policy marked as paid | Paid true; balance 0.96 ETH; reserves 0 ETH | Passed |

### Verification
The scripts check transaction receipts and contract state.
The compensation script also verifies the customer's balance change,
including the transaction gas cost.

Ganache's local time was advanced past the scheduled departure
to avoid waiting during the demonstration. The 120-minute delay
was simulated and submitted by the authorised reporter.

Compensation requires a claim transaction from the policy owner.
Reporting an eligible delay does not send the payment automatically.

### Evidence
Execution screenshots are stored in screenshots/, relative to this document.

## Remix functional and protection tests

These tests used Remix VM accounts, simulated flight information
and test ETH.

| Test | Expected behaviour | Recorded result |
| --- | --- | --- |
| Valid policy purchase | Accept the correct premium before departure | Policy created |
| Incorrect premium | Reject payment different from 0.01 ETH | Purchase rejected |
| Purchase after departure | Reject a departure timestamp in the past | Purchase rejected |
| Duplicate policy | Reject a second policy for the same customer and flight | Purchase rejected |
| Insufficient funds | Reject a purchase when funds cannot cover compensation | Rejected with "Insufficient available funds" |
| Report before departure | Reject a delay report before scheduled departure | Report rejected |
| Unauthorised reporter | Reject a report from another account | Report rejected |
| Repeated delay report | Prevent changes after a delay has been reported | Second report rejected |
| Claim before report | Reject a claim before flight information is reported | Rejected with "Delay not reported" |
| Claim by another account | Allow only the policy owner to claim | Rejected with "Only policy owner can claim" |
| Delay of 119 minutes | Reject compensation and release the flight's reserves | Claim rejected; reserves released |
| Delay of 120 minutes | Allow the owner to claim 0.05 ETH | Compensation paid |
| Delay of 121 minutes | Allow the owner to claim 0.05 ETH | Compensation paid |
| Repeated compensation claim | Prevent payment more than once | Rejected with "Compensation already paid" |

### Interpretation

The 119, 120 and 121-minute tests check the compensation boundary.
A delay of exactly 120 minutes qualifies.

Rejected transactions do not apply the attempted state changes.
Transaction gas costs may still apply when a reverted transaction
is mined.

These results cover the scenarios tested. They do not constitute
a complete security audit or prove suitability for real insurance.

### Limitations

- Flight information is simulated.
- The authorised reporter is a trusted central source.
- The contract cannot independently verify real flight delays.
- All payments use test ETH.
- The 120-minute threshold is a fictional project rule.