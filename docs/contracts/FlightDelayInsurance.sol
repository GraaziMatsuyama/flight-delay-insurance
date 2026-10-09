// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

contract FlightDelayInsurance {
    address public insurer;
    address public reporter;

    uint256 public constant PREMIUM = 0.01 ether;
    uint256 public constant COMPENSATION = 0.05 ether;
    uint256 public constant DELAY_THRESHOLD = 120;

    constructor(address reporterAddress) {
        require(
            reporterAddress != address(0),
            "Invalid reporter address"
        );

        insurer = msg.sender;
        reporter = reporterAddress;
    }
}