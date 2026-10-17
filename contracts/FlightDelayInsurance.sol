// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

contract FlightDelayInsurance {
    address public insurer;
    address public reporter;

    uint256 public constant PREMIUM = 0.01 ether;
    uint256 public constant COMPENSATION = 0.05 ether;
    uint256 public constant DELAY_THRESHOLD = 120;

    struct Flight {
        uint256 scheduledDeparture;
        uint256 delayMinutes;
        bool reported;
    }

    struct Policy {
        address customer;
        bytes32 flightId;
        bool paid;
    }

    uint256 public policyCount;
    uint256 public reservedFunds;

    mapping(bytes32 => Flight) public flights;
    mapping(uint256 => Policy) public policies;
    mapping(address => mapping(bytes32 => bool)) public hasPolicy;
    mapping(bytes32 => uint256) public flightPolicyCount;

    event DelayReported(
        bytes32 indexed flightId,
        uint256 delayMinutes
    );

    event ContractFunded(
        address indexed sender,
        uint256 amount
    );

    event PolicyPurchased(
        uint256 indexed policyId,
        address indexed customer,
        bytes32 indexed flightId
    );

      event CompensationPaid(
        uint256 indexed policyId,
        address indexed customer,
        uint256 amount
    );

    constructor(address reporterAddress) {
        require(
            reporterAddress != address(0),
            "Invalid reporter address"
        );

        insurer = msg.sender;
        reporter = reporterAddress;
    }

    function fundContract() external payable {
        require(
            msg.sender == insurer,
            "Only insurer can fund"
        );
        require(
            msg.value > 0,
            "Funding must be greater than zero"
        );

        emit ContractFunded(msg.sender, msg.value);
    }

    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }

    function buyPolicy(
        string calldata flightNumber,
        uint256 scheduledDeparture
    ) external payable {
        require(
            bytes(flightNumber).length > 0,
            "Flight number required"
        );
        require(
            scheduledDeparture > block.timestamp,
            "Purchase must be before departure"
        );
        require(
            msg.value == PREMIUM,
            "Incorrect premium"
        );

        bytes32 flightId = keccak256(
            abi.encode(flightNumber, scheduledDeparture)
        );

        require(
            !hasPolicy[msg.sender][flightId],
            "Policy already purchased"
        );
        require(
            !flights[flightId].reported,
            "Flight already reported"
        );
        require(
            address(this).balance >= reservedFunds + COMPENSATION,
            "Insufficient available funds"
        );

        flights[flightId].scheduledDeparture = scheduledDeparture;

        policyCount++;

        policies[policyCount] = Policy({
            customer: msg.sender,
            flightId: flightId,
            paid: false
        });

        hasPolicy[msg.sender][flightId] = true;
        reservedFunds += COMPENSATION;
        flightPolicyCount[flightId]++;

        emit PolicyPurchased(
            policyCount,
            msg.sender,
            flightId
        );
    }
        function reportDelay(
        bytes32 flightId,
        uint256 delayMinutes
    ) external {
        require(
            msg.sender == reporter,
            "Only reporter can report"
        );

        Flight storage flight = flights[flightId];

        require(
            flight.scheduledDeparture > 0,
            "Flight not found"
        );
        require(
            block.timestamp >= flight.scheduledDeparture,
            "Flight has not departed"
        );
        require(
            !flight.reported,
            "Delay already reported"
        );

        flight.delayMinutes = delayMinutes;
        flight.reported = true;

        if (delayMinutes < DELAY_THRESHOLD) {
            reservedFunds -=
                flightPolicyCount[flightId] * COMPENSATION;
        }

        emit DelayReported(flightId, delayMinutes);
    }
     function claimCompensation(uint256 policyId) external {
        require(
            policyId > 0 && policyId <= policyCount,
            "Policy not found"
        );

        Policy storage policy = policies[policyId];

        require(
            msg.sender == policy.customer,
            "Only policy owner can claim"
        );
        require(
            !policy.paid,
            "Compensation already paid"
        );

        Flight storage flight = flights[policy.flightId];

        require(
            flight.reported,
            "Delay not reported"
        );
        require(
            flight.delayMinutes >= DELAY_THRESHOLD,
            "Delay does not qualify"
        );

        policy.paid = true;
        reservedFunds -= COMPENSATION;

        (bool success, ) = payable(policy.customer).call{
            value: COMPENSATION
        }("");

        require(success, "Compensation transfer failed");

        emit CompensationPaid(
            policyId,
            policy.customer,
            COMPENSATION
        );
    }
}