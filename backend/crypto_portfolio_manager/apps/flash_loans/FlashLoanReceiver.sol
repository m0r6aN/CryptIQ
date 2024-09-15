pragma solidity ^0.6.6;
import "@aave/protocol-v2/contracts/flashloan/base/FlashLoanReceiverBase.sol";

contract FlashLoanRepayer is FlashLoanReceiverBase {

    address payable public owner;

    constructor(address _addressProvider) FlashLoanReceiverBase(_addressProvider) public {
        owner = msg.sender;
    }

    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
        // Logic to repay AAVE debt using the borrowed amount (amounts[0])

        // Repay the flash loan
        for (uint i = 0; i < assets.length; i++) {
            uint amountOwing = amounts[i].add(premiums[i]);
            IERC20(assets[i]).approve(address(LENDING_POOL), amountOwing);
        }
        return true;
    }

    function flashLoanRepayDebt(address asset, uint amount) external {
        address receiverAddress = address(this);
        address;
        assets[0] = asset;
        uint256;
        amounts[0] = amount;
        uint256;
        modes[0] = 0; // No debt mode

        LENDING_POOL.flashLoan(
            receiverAddress,
            assets,
            amounts,
            modes,
            address(this),
            params,
            0
        );
    }

    function withdraw() external {
        require(msg.sender == owner, "Not owner");
        owner.transfer(address(this).balance);
    }

    receive() external payable {}
}
