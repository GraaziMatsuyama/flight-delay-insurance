# flight-delay-insurance

CA1 Distributed Digital Transactions — flight delay insurance using a Solidity smart contract.

## About the project

A customer purchases a policy before the scheduled flight departure. An authorised reporter records the delay after departure.

If the delay is 120 minutes or more, the policy owner can request compensation. The contract checks the rules and transfers the payment.

Flight information is simulated and all payments use test ETH. The insurance conditions are fictional rules for this project.

## Main rules

- Each policy costs 0.01 test ETH.
- Compensation is 0.05 test ETH.
- A delay of 120 minutes or more qualifies.
- Policies must be purchased before departure.
- Each customer can buy only one policy per flight.
- The contract reserves enough funds to cover each policy.
- Only the authorised reporter can report a delay.
- A recorded delay cannot be changed.
- Only the policy owner can claim compensation.
- Each policy can receive compensation only once.

## Tools used

- Solidity and Remix IDE
- Ganache 7.9.2
- Python 3.14.6
- web3.py 8.0.0

## Compilation settings

- Solidity compiler: 0.8.34+commit.80d5c536
- EVM target: Shanghai
- Optimizer: disabled
- Optimizer runs: 200, inactive while optimization is disabled

## Project structure

- contracts/: Solidity source code.
- scripts/: Python scripts for the demonstration.
- build/: compiled ABI and creation bytecode.
- docs/screenshots/: execution evidence.
- docs/testing.md: test results and limitations.
- requirements.md: project requirements.
- design.md: project design.
- requirements.txt: Python dependencies.

## Progress

The smart contract has been implemented and manually tested in Remix.

The complete Python and Ganache workflow has also been tested: deployment, funding, policy purchase, delay reporting and compensation.

Tests include delays of 119, 120 and 121 minutes, access restrictions, duplicate purchases, repeated claims and insufficient contract funds.

## Limitations

The project relies on a trusted reporter and cannot independently verify real flight information.

Compensation requires a claim transaction from the policy owner. The prototype has not undergone a complete security audit.

## Running the demonstration

Requirements: Node.js with npm, Python and Bash.

From the repository root, create the Python environment
and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

In a separate terminal, start Ganache and leave it running:

```bash
npx ganache@7.9.2
```

Back in the repository terminal, run:

```bash
bash scripts/run_demo.sh
```

The shell script checks the connection, deploys a new contract,
funds it, purchases a policy, reports a simulated delay
and claims compensation.

Expected final results:
- Compensation: 0.05 test ETH.
- Policy paid: true.
- Contract balance: 0.96 ETH.
- Reserved funds: 0 ETH.

Each run creates a new contract instance and updates the local
deployment and purchase files.

The demonstration advances Ganache's local blockchain time.
It does not change the computer's clock.

### Using an existing Python environment

To use the environment created in the home directory:

```bash
PYTHON_BIN="$HOME/.venv/bin/python" bash scripts/run_demo.sh
```

### Restarting Ganache

The startup command above does not persist blockchain state.
After restarting Ganache, run the demonstration again to create
and fund a new contract.