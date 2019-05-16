config = {'abi': [{'constant': True, 'inputs': [], 'name': 'termLen', 'outputs': [{'name': '', 'type': 'uint256'}],
                       'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [
        {'name': '_numOfCampaign', 'type': 'uint256'}, {'name': '_cpuNonce', 'type': 'uint64'},
        {'name': '_cpuBlockNumber', 'type': 'uint256'}, {'name': '_memoryNonce', 'type': 'uint64'},
        {'name': '_memoryBlockNumber', 'type': 'uint256'}], 'name': 'claimCampaign', 'outputs': [], 'payable': True,
                                                                                          'stateMutability': 'payable',
                                                                                          'type': 'function'},
                      {'constant': True, 'inputs': [{'name': '_termIdx', 'type': 'uint256'}], 'name': 'candidatesOf',
                       'outputs': [{'name': '', 'type': 'address[]'}], 'payable': False, 'stateMutability': 'view',
                       'type': 'function'},
                      {'constant': True, 'inputs': [], 'name': 'termIdx', 'outputs': [{'name': '', 'type': 'uint256'}],
                       'payable': False, 'stateMutability': 'view', 'type': 'function'},
                      {'constant': True, 'inputs': [], 'name': 'minNoc', 'outputs': [{'name': '', 'type': 'uint256'}],
                       'payable': False, 'stateMutability': 'view', 'type': 'function'},
                      {'constant': True, 'inputs': [], 'name': 'withdrawTermIdx',
                       'outputs': [{'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view',
                       'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'numPerRound',
                                             'outputs': [{'name': '', 'type': 'uint256'}], 'payable': False,
                                             'stateMutability': 'view', 'type': 'function'},
                      {'constant': True, 'inputs': [], 'name': 'viewLen', 'outputs': [{'name': '', 'type': 'uint256'}],
                       'payable': False, 'stateMutability': 'view', 'type': 'function'},
                      {'constant': False, 'inputs': [{'name': '_maxNoc', 'type': 'uint256'}], 'name': 'updateMaxNoc',
                       'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'},
                      {'constant': False, 'inputs': [{'name': '_minNoc', 'type': 'uint256'}], 'name': 'updateMinNoc',
                       'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'},
                      {'constant': False, 'inputs': [{'name': '_addr', 'type': 'address'}], 'name': 'setAdmissionAddr',
                       'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'},
                      {'constant': False, 'inputs': [{'name': '_termLen', 'type': 'uint256'}], 'name': 'updateTermLen',
                       'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'},
                      {'constant': False, 'inputs': [{'name': '_viewLen', 'type': 'uint256'}], 'name': 'updateViewLen',
                       'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'},
                      {'constant': True, 'inputs': [{'name': '_candidate', 'type': 'address'}],
                       'name': 'candidateInfoOf',
                       'outputs': [{'name': '', 'type': 'uint256'}, {'name': '', 'type': 'uint256'},
                                   {'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view',
                       'type': 'function'},
                      {'constant': True, 'inputs': [], 'name': 'maxNoc', 'outputs': [{'name': '', 'type': 'uint256'}],
                       'payable': False, 'stateMutability': 'view', 'type': 'function'},
                      {'constant': False, 'inputs': [{'name': '_addr', 'type': 'address'}], 'name': 'setRnodeInterface',
                       'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'},
                      {'constant': False, 'inputs': [], 'name': 'updateCandidateStatus', 'outputs': [], 'payable': True,
                       'stateMutability': 'payable', 'type': 'function'}, {
                          'inputs': [{'name': '_admissionAddr', 'type': 'address'},
                                     {'name': '_rnodeAddr', 'type': 'address'}], 'payable': False,
                          'stateMutability': 'nonpayable', 'type': 'constructor'},
                      {'payable': True, 'stateMutability': 'payable', 'type': 'fallback'}, {'anonymous': False,
                                                                                            'inputs': [
                                                                                                {'indexed': False,
                                                                                                 'name': 'candidate',
                                                                                                 'type': 'address'},
                                                                                                {'indexed': False,
                                                                                                 'name': 'startTermIdx',
                                                                                                 'type': 'uint256'},
                                                                                                {'indexed': False,
                                                                                                 'name': 'stopTermIdx',
                                                                                                 'type': 'uint256'}],
                                                                                            'name': 'ClaimCampaign',
                                                                                            'type': 'event'},
                      {'anonymous': False, 'inputs': [{'indexed': False, 'name': 'candidate', 'type': 'address'},
                                                      {'indexed': False, 'name': 'payback', 'type': 'uint256'}],
                       'name': 'QuitCampaign', 'type': 'event'},
                      {'anonymous': False, 'inputs': [], 'name': 'ViewChange', 'type': 'event'}],
              'bin': '608060405260006001556003600255600c600355600254600354026004556001600555600a60065560006007556001600860006101000a81548160ff02191690831515021790555034801561005357600080fd5b5060405160408061178d8339810180604052810190808051906020019092919080519060200190929190505050336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555081600b60006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555080600c60006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555061016760045460014303610174640100000000026113cd179091906401000000009004565b600781905550505061018f565b600080828481151561018257fe5b0490508091505092915050565b6115ef8061019e6000396000f3006080604052600436106100f1576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806314b5980e146100f357806314b90a021461011e5780631984ab001461017a57806335805726146101fc5780633a713e3714610227578063488b87e5146102525780634b6b164b1461027d57806368f237a1146102a85780638cb59532146102d3578063a7e1f08b14610300578063c0e9e35e1461032d578063c351d0a514610370578063cd60e2171461039d578063db438269146103ca578063e2b281581461042f578063f2aaabdd1461045a578063fcf503f81461049d575b005b3480156100ff57600080fd5b506101086104a7565b6040518082815260200191505060405180910390f35b61017860048036038101908080359060200190929190803567ffffffffffffffff16906020019092919080359060200190929190803567ffffffffffffffff169060200190929190803590602001909291905050506104ad565b005b34801561018657600080fd5b506101a560048036038101908080359060200190929190505050610c9c565b6040518080602001828103825283818151815260200191508051906020019060200280838360005b838110156101e85780820151818401526020810190506101cd565b505050509050019250505060405180910390f35b34801561020857600080fd5b50610211610d40565b6040518082815260200191505060405180910390f35b34801561023357600080fd5b5061023c610d46565b6040518082815260200191505060405180910390f35b34801561025e57600080fd5b50610267610d4c565b6040518082815260200191505060405180910390f35b34801561028957600080fd5b50610292610d52565b6040518082815260200191505060405180910390f35b3480156102b457600080fd5b506102bd610d58565b6040518082815260200191505060405180910390f35b3480156102df57600080fd5b506102fe60048036038101908080359060200190929190505050610d5e565b005b34801561030c57600080fd5b5061032b60048036038101908080359060200190929190505050610dc3565b005b34801561033957600080fd5b5061036e600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610e28565b005b34801561037c57600080fd5b5061039b60048036038101908080359060200190929190505050610ec7565b005b3480156103a957600080fd5b506103c860048036038101908080359060200190929190505050610f40565b005b3480156103d657600080fd5b5061040b600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610fb9565b60405180848152602001838152602001828152602001935050505060405180910390f35b34801561043b57600080fd5b50610444611094565b6040518082815260200191505060405180910390f35b34801561046657600080fd5b5061049b600480360381019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919050505061109a565b005b6104a5611139565b005b60035481565b600080600860009054906101000a900460ff161561050257600a6104df600454600143036113cd90919063ffffffff16565b036007819055506000600860006101000a81548160ff0219169083151502179055505b60011515600c60009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1663a8f07697336040518263ffffffff167c0100000000000000000000000000000000000000000000000000000000028152600401808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001915050602060405180830381600087803b1580156105c357600080fd5b505af11580156105d7573d6000803e3d6000fd5b505050506040513d60208110156105ed57600080fd5b81019080805190602001909291905050501515141515610675576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260128152602001807f6e6f7420524e6f646520627920726e6f6465000000000000000000000000000081525060200191505060405180910390fd5b600b60009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16633395492e87878787336040518663ffffffff167c0100000000000000000000000000000000000000000000000000000000028152600401808667ffffffffffffffff1667ffffffffffffffff1681526020018581526020018467ffffffffffffffff1667ffffffffffffffff1681526020018381526020018273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200195505050505050602060405180830381600087803b15801561077a57600080fd5b505af115801561078e573d6000803e3d6000fd5b505050506040513d60208110156107a457600080fd5b81019080805190602001909291905050501515610829576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260198152602001807f637075206f72206d656d6f7279206e6f74207061737365642e0000000000000081525060200191505060405180910390fd5b600554871015801561083d57506006548711155b15156108b1576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252601d8152602001807f6e756d206f662063616d706169676e206f7574206f662072616e67652e00000081525060200191505060405180910390fd5b6108b9611139565b3391506000600960008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000015414151561099c576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260378152602001807f706c6561736520776169746520756e74696c20796f7572206c61737420726f7581526020017f6e6420656e64656420616e642074727920616761696e2e00000000000000000081525060400191505060405180910390fd5b86600960008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600001819055506109f8600180546113e890919063ffffffff16565b600960008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060010181905550610a9387600960008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600101546113e890919063ffffffff16565b600960008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060020181905550600960008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206001015490505b600960008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060020154811015610b9c57610b8e82600a600084815260200190815260200160002061140690919063ffffffff16565b508080600101915050610b1f565b7f8d468194bdd18296bee5d126aa15cc492d26bdf22a0585c4a47ec4490d3a0fcf82600960008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060010154600960008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060020154604051808473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001838152602001828152602001935050505060405180910390a150505050505050565b6060600a6000838152602001908152602001600020600101805480602002602001604051908101604052809291908181526020018280548015610d3457602002820191906000526020600020905b8160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019060010190808311610cea575b50505050509050919050565b60015481565b60055481565b60075481565b60045481565b60025481565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141515610db957600080fd5b8060068190555050565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141515610e1e57600080fd5b8060058190555050565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141515610e8357600080fd5b80600b60006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141515610f2257600080fd5b80600381905550610f37600354600254611532565b60048190555050565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141515610f9b57600080fd5b80600281905550610fb0600354600254611532565b60048190555050565b6000806000600960008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060000154600960008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060010154600960008773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600201549250925092509193909250565b60065481565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415156110f557600080fd5b80600c60006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b600080600061114661156d565b600154600754101515611158576113c8565b5b6001546007541115156113c757600a60006007548152602001908152602001600020600101805490509250600091505b828210156113b057600a60006007548152602001908152602001600020600101828154811015156111b657fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690506000600960008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600001541415611233576113a3565b611280600960008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000015460016115aa565b600960008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600001819055506000600960008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000015414156113a2576000600960008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600101819055506000600960008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600201819055505b5b8180600101925050611189565b600760008154809291906001019190505550611159565b5b505050565b60008082848115156113db57fe5b0490508091505092915050565b60008082840190508381101515156113fc57fe5b8091505092915050565b60008260000160008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff1615611465576000905061152c565b60018360000160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff021916908315150217905550826001018290806001815401808255809150509060018203906000526020600020016000909192909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050600190505b92915050565b60008060008414156115475760009150611566565b828402905082848281151561155857fe5b0414151561156257fe5b8091505b5092915050565b600043905060008114156115885760006001819055506115a7565b6115a0600454600183036113cd90919063ffffffff16565b6001819055505b50565b60008282111515156115b857fe5b8183039050929150505600a165627a7a7230582051050722c69054c7e341561945adf0dcf3f532d10a6e715b3584de9965bc130e0029'}
