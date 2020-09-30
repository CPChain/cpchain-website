"""

生成测试数据

"""

import logging
import logging.handlers
import time

import hexbytes
from pymongo import DESCENDING, MongoClient


DAY_SECENDS = 60 * 60 * 24
REFRESH_INTERVAL = 3

# mongodb
mongoHost = "127.0.0.1"
port = 27017

client = MongoClient(host=mongoHost, port=port)
uname = "uname"
pwd = "password"
db = client['cpchain']
db.authenticate(uname, pwd)

b_collection = client['cpchain']['blocks']
address_collection = client['cpchain']['address']
contract_collection = client['cpchain']['contract']
event_collection = client['cpchain']['event']
impeach_collection = client['cpchain']['impeach']
tx_collection = client['cpchain']['txs']

num_collection = client['cpchain']['num']

if num_collection.estimated_document_count() == 0:
    num_collection.insert_one({"type": "tps", "tps": 0.05})
    num_collection.insert_one({"type": "bps", "bps": 0.1})

proposer_col = client['cpchain']['proposer']

if proposer_col.estimated_document_count() == 0:
    proposer_col.insert_one({"BlockNumber": 3977306, "Proposer": "0x73ae2b32ef3fad80707d4da0f49c675d3efc727c", "ProposerIndex": 1, "Proposers": ["0xf42c53ada41e0d7dc09833f318b588f51d204671", "0x73ae2b32ef3fad80707d4da0f49c675d3efc727c", "0x1786dd90fccbbedfafd8b6fb16523af6375bdfd1", "0x04f0121479e8563f73846e8dce659aa397542f4f", "0x8ab63651e6ce7eed40af33276011a5e2e1a533a2",
                                                                                                                                                 "0x2d55e6c246b42f50c1b03e6487f2dcd90e7ec7b8", "0x3160b1b5ed4eb77560af85c5c0835e6188f69147", "0x84d2a16b498c7d259d8b7859b571f7ca75455fac", "0x8c65cb8568c4945d4b419af9066874178f19ba43", "0x95498631be17339225bb4039b800a4d4294e8cf4", "0x501f6cf7b2437671d770998e3b785474878fef1d", "0x6093ed380b7c8e6c201d8fc4d41ebbf15788f7fe"], "Term": 110480, "TermLen": 12, "View": 2})

block = {
    "dpor": {
        "seal": "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "sigs": [
            "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        ],
        "proposers": [
            "0x50f8c76f6d8442c54905c74245ae163132b9f4ae",
            "0x8ab63651e6ce7eed40af33276011a5e2e1a533a2",
            "0x501f6cf7b2437671d770998e3b785474878fef1d",
            "0x9508e430ce672750bcf6bef9c4c0adf303b28c5c",
            "0x049295e2e925cec28ddeeb63507e654b6d317423",
            "0x8c65cb8568c4945d4b419af9066874178f19ba43",
            "0x4d1f1d14f303b746121564e3295e2957e74ea5d2",
            "0x73ae2b32ef3fad80707d4da0f49c675d3efc727c",
            "0x5a55d5ef67c047b5d748724f7401781ed0af65ed",
            "0x1f077085dfdfa4a65f8870e50348f277d6fcd97c",
            "0xcb6fb6a201d6c126f80053fe17ca45188e24fe2f",
            "0xfaf2a2cdc4da310b52ad7d8d86e8c1bd5d4c0bd0"
        ],
        "validators": [
            "0x2effd798690059ed313fa7d08483bcfa7ea637be",
            "0x1f12dc7132c31dd26dfac3754b3a7ea0da1ea352",
            "0xca9463aa4b1157681421c72e052d2cf8b6498a38",
            "0xd08975bb4c17c8139cf5107e1fd896d46b7a848a",
            "0xce5eb5797e457cfa99f0bf2c994c46614bfb4feb",
            "0x15b5a0709ae8cf751377bf9e26b8340c7bb9162b",
            "0x1e693ea09b1593bd3c795186806121f5b69371b6"
        ]
    },
    "extraData": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "gasLimit": 100000000,
    "gasUsed": 0,
    "hash": "0xf70bf47d2629b1e9e9f900b0eb3b73e7e93c31b330d04c0029557d2ad065282a",
    "logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "miner": "0x0000000000000000000000000000000000000000",
    "impeachProposer": "0x9508e430ce672750bcf6bef9c4c0adf303b28c5c",
    "number": 0,
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "receiptsRoot": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
    "size": 1411,
    "stateRoot": "0x2f243f9569d61f57f34cee1f9ed75991defcdde1795114e0abe6d3319bc7bd55",
    "timestamp": 1553754594,
    "transactions": [],
    "transactionsRoot": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
    "reward": 0
}

tx = {
    "blockHash": "0xb899c7c5064693980ff43c3e015d4c83bad6f9ec4e621346b7485a0b7c173757",
    "blockNumber": 53,
    "from": "0x66961306fd78d39a4604167f59b25697bdad05c5",
    "gas": 955452,
    "gasPrice": 18000000000,
    "hash": "0x90785c751f8f908ba018ab58937347b673e785c0aba08202f965f39f0910d02b",
    "type": "0x0",
    "input": "0x60806040526117706001908155692a5a058fc295ed00000060025560038190556007805460ff1916909117905534801561003857600080fd5b5060008054600160a060020a03191633179055610bc18061005a6000396000f3006080604052600436106100fb5763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416630b443f4281146101005780630f3a9f6514610127578063113c8498146101415780631627905514610156578063238dafe01461018b578063367edd32146101a057806338e771ab146101b5578063595aa13d146101ca5780635f86d4ca14610204578063894ba8331461021c578063975dd4b214610231578063a8f0769714610249578063aae80f781461026a578063b7b3e9da14610275578063d5601e9f1461028a578063e508bb851461029f578063ef78d4fd14610304578063fa89401a14610319575b600080fd5b34801561010c57600080fd5b5061011561033a565b6040$051918252519081900360200190f35b34801561013357600080fd5b5061013f600435610341565b005b34801561014d57600080fd5b5061013f61035d565b34801561016257600080fd5b50610177600160a060020a036004351661042e565b604080519115158252519081900360200190f35b34801561019757600080fd$b50610177610436565b3480156101ac57600080fd5b5061013f61043f565b3480156101c157600080fd5b5061013f610465565b3480156101d657600080fd5b506101eb600160a060020a03600435166105b6565b6040805192835260208301919091528051918290030190f35b34801561021057600080fd5b5061013f60$4356105cf565b34801561022857600080fd5b5061013f6105eb565b34801561023d57600080fd5b5061013f60043561060e565b34801561025557600080fd5b50610177600160a060020a036004351661062a565b61013f600435610643565b34801561028157600080fd5b506101156107cd565b34801561029657600080$d5b506101156107d3565b3480156102ab57600080fd5b506102b46107d9565b60408051602080825283518183015283519192839290830191858101910280838360005b838110156102f05781810151838201526020016102d8565b505050509050019250505060405180910390f35b34801561031057600080fd5b506101$56107ea565b34801561032557600080fd5b5061013f600160a060020a03600435166107f0565b6006545b90565b600054600160a060020a0316331461035857600080fd5b600155565b61036e60043363ffffffff6108de16565b151561037957600080fd5b60018054336000908152600860205260409020909101544291$1111561039e57600080fd5b3360008181526008602052604080822054905181156108fc0292818181858888f193505050501580156103d5573d6000803e3d6000fd5b50336000818152600860205260408120556103f89060049063ffffffff6108fd16565b506040805133815290517f602a2a9c94f70293aa2be9077f0b$dc89d388bc293fdbcd968274f43494c380d9181900360200190a1565b6000903b1190565b60075460ff1681565b600054600160a060020a0316331461045657600080fd5b6007805460ff19166001179055565b60008054819081908190600160a060020a0316331461048357600080fd5b6006549350600092505b838310$5610573576006805460009081106104a457fe5b6000918252602080832090910154600160a060020a0316808352600890915260408083205490519194509250839183156108fc02918491818181858888f193505050501580156104f8573d6000803e3d6000fd5b50600160a060020a038216600090815260086020526040$1205561052360048363ffffffff6108fd16565b5060408051600160a060020a03841681526020810183905281517f3914ba80eb00486e7a58b91fb4795283df0c5b507eea9cf7c77cce26cc70d25c929181900390910190a160019092019161048d565b6006541561057d57fe5b6040805185815290517fb65ebb6b17695b$a5612c7a0f6f60e649c02ba24b36b546b8d037e98215fdb8d9181900360200190a150505050565b6008602052600090815260409020805460019091015482565b600054600160a060020a031633146105e657600080fd5b600355565b600054600160a060020a0316331461060257600080fd5b6007805460ff1916905556$b600054600160a060020a0316331461062557600080fd5b600255565b600061063d60048363ffffffff6108de16565b92915050565b60075460ff16151561065457600080fd5b60035481101561066357600080fd5b61066c3361042e565b156106fe57604080517f08c379a0000000000000000000000000000000000000$0000000000000000000815260206004820152602a60248201527f706c65617365206e6f742075736520636f6e74726163742063616c6c2074686960448201527f732066756e6374696f6e00000000000000000000000000000000000000000000606482015290519081900360840190fd5b61070f60043363ffffffff6108$e16565b1561071957600080fd5b60025434101561072857600080fd5b33600090815260086020526040902054610748903463ffffffff610a4316565b336000818152600860205260409020918255426001909201919091556107769060049063ffffffff610a5916565b5033600081815260086020908152604091829020$05460019091015483519485529184015282820152517f586bfaa7a657ad9313326c9269639546950d589bd479b3d6928be469d6dc29039181900360600190a150565b60025481565b60035481565b60606107e56004610ae8565b905090565b60015481565b60008054600160a060020a0316331461080857600080fd5b61$81960048363ffffffff6108de16565b151561082457600080fd5b50600160a060020a03811660008181526008602052604080822054905190929183156108fc02918491818181858888f1935050505015801561086a573d6000803e3d6000fd5b50600160a060020a03821660009081526008602052604081205561089560$48363ffffffff6108fd16565b5060408051600160a060020a03841681526020810183905281517f3914ba80eb00486e7a58b91fb4795283df0c5b507eea9cf7c77cce26cc70d25c929181900390910190a15050565b600160a060020a03166000908152602091909152604090205460ff1690565b600160a060020a038116$0009081526020839052604081205481908190819060ff16151561092e5760009350610a3a565b600160a060020a038516600090815260208781526040808320805460ff1916905560028901805460018b019093529220549094509250600019840184811061097257fe5b6000918252602090912001546002870180546001$0a060020a03909216925082918490811061099d57fe5b6000918252602080832091909101805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a039485161790559183168152600188019091526040902082905560028601805460001985019081106109f957fe5b600091825260209091200180$473ffffffffffffffffffffffffffffffffffffffff1916905560028601805490610a34906000198301610b4e565b50600193505b50505092915050565b600082820183811015610a5257fe5b9392505050565b600160a060020a03811660009081526020839052604081205460ff1615610a825750600061063d565b5060$160a060020a0316600081815260208381526040808320805460ff19166001908117909155600286018054968201845291842086905585810182559083529120909201805473ffffffffffffffffffffffffffffffffffffffff1916909117905590565b606081600201805480602002602001604051908101604052809291$08181526020018280548015610b4257602002820191906000526020600020905b8154600160a060020a03168152600190910190602001808311610b24575b50505050509050919050565b815481835581811115610b7257600083815260209020610b72918101908301610b77565b505050565b61033e91905b8082111561$b915760008155600101610b7d565b50905600a165627a7a7230582072371a09b1de7f97b9d6e51430a0b38a132ec0b15a9341f7280042b7161e61120029",
    "nonce": 0,
    "to": "0x66961306fd78d39a4604167f59b25697bdad05c5",
    "transactionIndex": 0,
    "value": 0,
    "v": 710,
    "r": "0x19d8cd1e87a0268f814c61c2e023ef0554c0ce81d87811c47e8442c9e536d5bb",
    "s": "0x2a09d6e5daae3ffb7f360a98a26fba13012cffe0662498f628cdbec7d1b90091",
    "creator": "0x66961306fD78d39a4604167f59b25697BDAD05c5",
    "isContract": False,
    "code": "0x6080604052600436106100fb5763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416630b443f4281146101005780630f3a9f6514610127578063113c8498146101415780631627905514610156578063238dafe01461018b578063367edd32146101a057806338e771ab146101b5578063595aa13d146101ca5780635f86d4ca14610204578063894ba8331461021c578063975dd4b214610231578063a8f0769714610249578063aae80f781461026a578063b7b3e9da14610275578063d5601e9f1461028a578063e508bb851461029f578063ef78d4fd14610304578063fa89401a14610319575b600080fd5b34801561010c57600080fd5b5061011561033a565b60408051918252519081900360200190f35b34801561013357600080fd5b5061013f600435610341565b005b34801561014d57600080fd5b5061013f61035d565b34801561016257600080fd5b50610177600160a060020a036004351661042e565b604080519115158252519081900360200190f35b34801561019757600080fd5b50610177610436565b3480156101ac57600080fd5b5061013f61043f565b3480156101c157600080fd5b5061013f610465565b3480156101d657600080fd5b506101eb600160a060020a03600435166105b6565b6040805192835260208301919091528051918290030190f35b34801561021057600080fd5b5061013f6004356105cf565b34801561022857600080fd5b5061013f6105eb565b34801561023d57600080fd5b5061013f60043561060e565b34801561025557600080fd5b50610177600160a060020a036004351661062a565b61013f600435610643565b34801561028157600080fd5b506101156107cd565b34801561029657600080fd5b506101156107d3565b3480156102ab57600080fd5b506102b46107d9565b60408051602080825283518183015283519192839290830191858101910280838360005b838110156102f05781810151838201526020016102d8565b505050509050019250505060405180910390f35b34801561031057600080fd5b506101156107ea565b34801561032557600080fd5b5061013f600160a060020a03600435166107f0565b6006545b90565b600054600160a060020a0316331461035857600080fd5b600155565b61036e60043363ffffffff6108de16565b151561037957600080fd5b6001805433600090815260086020526040902090910154429101111561039e57600080fd5b3360008181526008602052604080822054905181156108fc0292818181858888f193505050501580156103d5573d6000803e3d6000fd5b50336000818152600860205260408120556103f89060049063ffffffff6108fd16565b506040805133815290517f602a2a9c94f70293aa2be9077f0b2dc89d388bc293fdbcd968274f43494c380d9181900360200190a1565b6000903b1190565b60075460ff1681565b600054600160a060020a0316331461045657600080fd5b6007805460ff19166001179055565b60008054819081908190600160a060020a0316331461048357600080fd5b6006549350600092505b83831015610573576006805460009081106104a457fe5b6000918252602080832090910154600160a060020a0316808352600890915260408083205490519194509250839183156108fc02918491818181858888f193505050501580156104f8573d6000803e3d6000fd5b50600160a060020a03821660009081526008602052604081205561052360048363ffffffff6108fd16565b5060408051600160a060020a03841681526020810183905281517f3914ba80eb00486e7a58b91fb4795283df0c5b507eea9cf7c77cce26cc70d25c929181900390910190a160019092019161048d565b6006541561057d57fe5b6040805185815290517fb65ebb6b17695b3a5612c7a0f6f60e649c02ba24b36b546b8d037e98215fdb8d9181900360200190a150505050565b6008602052600090815260409020805460019091015482565b600054600160a060020a031633146105e657600080fd5b600355565b600054600160a060020a0316331461060257600080fd5b6007805460ff19169055565b600054600160a060020a0316331461062557600080fd5b600255565b600061063d60048363ffffffff6108de16565b92915050565b60075460ff16151561065457600080fd5b60035481101561066357600080fd5b61066c3361042e565b156106fe57604080517f08c379a000000000000000000000000000000000000000000000000000000000815260206004820152602a60248201527f706c65617365206e6f742075736520636f6e74726163742063616c6c2074686960448201527f732066756e6374696f6e00000000000000000000000000000000000000000000606482015290519081900360840190fd5b61070f60043363ffffffff6108de16565b1561071957600080fd5b60025434101561072857600080fd5b33600090815260086020526040902054610748903463ffffffff610a4316565b336000818152600860205260409020918255426001909201919091556107769060049063ffffffff610a5916565b5033600081815260086020908152604091829020805460019091015483519485529184015282820152517f586bfaa7a657ad9313326c9269639546950d589bd479b3d6928be469d6dc29039181900360600190a150565b60025481565b60035481565b60606107e56004610ae8565b905090565b60015481565b60008054600160a060020a0316331461080857600080fd5b61081960048363ffffffff6108de16565b151561082457600080fd5b50600160a060020a03811660008181526008602052604080822054905190929183156108fc02918491818181858888f1935050505015801561086a573d6000803e3d6000fd5b50600160a060020a03821660009081526008602052604081205561089560048363ffffffff6108fd16565b5060408051600160a060020a03841681526020810183905281517f3914ba80eb00486e7a58b91fb4795283df0c5b507eea9cf7c77cce26cc70d25c929181900390910190a15050565b600160a060020a03166000908152602091909152604090205460ff1690565b600160a060020a03811660009081526020839052604081205481908190819060ff16151561092e5760009350610a3a565b600160a060020a038516600090815260208781526040808320805460ff1916905560028901805460018b019093529220549094509250600019840184811061097257fe5b600091825260209091200154600287018054600160a060020a03909216925082918490811061099d57fe5b6000918252602080832091909101805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a039485161790559183168152600188019091526040902082905560028601805460001985019081106109f957fe5b6000918252602090912001805473ffffffffffffffffffffffffffffffffffffffff1916905560028601805490610a34906000198301610b4e565b50600193505b50505092915050565b600082820183811015610a5257fe5b9392505050565b600160a060020a03811660009081526020839052604081205460ff1615610a825750600061063d565b50600160a060020a0316600081815260208381526040808320805460ff19166001908117909155600286018054968201845291842086905585810182559083529120909201805473ffffffffffffffffffffffffffffffffffffffff1916909117905590565b606081600201805480602002602001604051908101604052809291908181526020018280548015610b4257602002820191906000526020600020905b8154600160a060020a03168152600190910190602001808311610b24575b50505050509050919050565b815481835581811115610b7257600083815260209020610b72918101908301610b77565b505050565b61033e91905b80821115610b915760008155600101610b7d565b50905600a165627a7a7230582072371a09b1de7f97b9d6e51430a0b38a132ec0b15a9341f7280042b7161e61120029",
    "contractAddress": "0x76130DA5aA1851313a7555D3735BED76029560DA",
    "gasUsed": 955452,
    "status": 1,
    "timestamp": 1561606120.527,
    "txfee": 0.017198136
}

if tx_collection.estimated_document_count() == 0:
    tx_collection.insert_one(tx)

if b_collection.estimated_document_count() == 0:
    b_collection.insert_one(block)
