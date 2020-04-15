"""

sync all data from congress constract

"""

from cpc_fusion import Web3
from cpchain_test.config import cfg
import django
import logging
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cpchain_test.settings')
django.setup()

from community.models import Congress
from log import get_log

# import models

log = get_log('sync-congress')

host = cfg["chain"]["ip"]
port = cfg["chain"]["port"]
address = cfg['community']['congress']

log.info(f"chain rpc interface: http://{host}:{port}")
log.info(f'congress constract\'s address is {address}')

cf = Web3(Web3.HTTPProvider(f'http://{host}:{port}'))

# CongressABI is the input ABI used to generate the binding from.
abi = "[{\"constant\":false,\"inputs\":[{\"name\":\"_period\",\"type\":\"uint256\"}],\"name\":\"setPeriod\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"addr\",\"type\":\"address\"}],\"name\":\"isContract\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"threshold\",\"type\":\"uint256\"}],\"name\":\"setCongressThreshold\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"enabled\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"addr\",\"type\":\"address\"}],\"name\":\"isInCongress\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"enableContract\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"refundAll\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"congressThreshold\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"version\",\"type\":\"uint256\"}],\"name\":\"joinCongress\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"\",\"type\":\"address\"}],\"name\":\"Participants\",\"outputs\":[{\"name\":\"lockedDeposit\",\"type\":\"uint256\"},{\"name\":\"lockedTime\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"version\",\"type\":\"uint256\"}],\"name\":\"setSupportedVersion\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"getCongressNum\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"getCongress\",\"outputs\":[{\"name\":\"\",\"type\":\"address[]\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"quitCongress\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"disableContract\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"supportedVersion\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"period\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"investor\",\"type\":\"address\"}],\"name\":\"refund\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"who\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"lockedDeposit\",\"type\":\"uint256\"},{\"indexed\":false,\"name\":\"lockedTime\",\"type\":\"uint256\"}],\"name\":\"Join\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"who\",\"type\":\"address\"}],\"name\":\"Quit\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"who\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"amount\",\"type\":\"uint256\"}],\"name\":\"ownerRefund\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"numOfInvestor\",\"type\":\"uint256\"}],\"name\":\"ownerRefundAll\",\"type\":\"event\"}]"

# CongressBin is the compiled bytecode used for deploying new contracts.
binary = '0x60806040526276a7006001908155692a5a058fc295ed00000060025560038190556007805460ff1916909117905534801561003957600080fd5b5060008054600160a060020a03191633179055610be88061005b6000396000f3006080604052600436106100fb5763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416630f3a9f658114610100578063162790551461011a57806322ab6c3d1461014f578063238dafe01461016757806327bd4ba71461017c578063367edd321461019d57806338e771ab146101b257806339fad16e146101c757806351f5f87a146101ee578063595aa13d146101f95780635f86d4ca146102335780636656b3751461024b5780636a96b9a51461026057806373a5c457146102c5578063894ba833146102da578063d5601e9f146102ef578063ef78d4fd14610304578063fa89401a14610319575b600080fd5b34801561010c57600080fd5b5061011860043561033a565b005b34801561012657600080fd5b5061013b600160a060020a0360043516610366565b604080519115158252519081900360200190f35b34801561015b57600080fd5b5061011860043561036e565b34801561017357600080fd5b5061013b6103a1565b34801561018857600080fd5b5061013b600160a060020a03600435166103aa565b3480156101a957600080fd5b506101186103c3565b3480156101be57600080fd5b506101186103e9565b3480156101d357600080fd5b506101dc61053a565b60408051918252519081900360200190f35b610118600435610540565b34801561020557600080fd5b5061021a600160a060020a03600435166106ca565b6040805192835260208301919091528051918290030190f35b34801561023f57600080fd5b506101186004356106e3565b34801561025757600080fd5b506101dc6106ff565b34801561026c57600080fd5b50610275610706565b60408051602080825283518183015283519192839290830191858101910280838360005b838110156102b1578181015183820152602001610299565b505050509050019250505060405180910390f35b3480156102d157600080fd5b50610118610717565b3480156102e657600080fd5b506101186107e8565b3480156102fb57600080fd5b506101dc61080b565b34801561031057600080fd5b506101dc610811565b34801561032557600080fd5b50610118600160a060020a0360043516610817565b600054600160a060020a0316331461035157600080fd5b6201518081111561036157600080fd5b600155565b6000903b1190565b600054600160a060020a0316331461038557600080fd5b692a5a058fc295ed00000081101561039c57600080fd5b600255565b60075460ff1681565b60006103bd60048363ffffffff61090516565b92915050565b600054600160a060020a031633146103da57600080fd5b6007805460ff19166001179055565b60008054819081908190600160a060020a0316331461040757600080fd5b6006549350600092505b838310156104f75760068054600090811061042857fe5b6000918252602080832090910154600160a060020a0316808352600890915260408083205490519194509250839183156108fc02918491818181858888f1935050505015801561047c573d6000803e3d6000fd5b50600160a060020a0382166000908152600860205260408120556104a760048363ffffffff61092416565b5060408051600160a060020a03841681526020810183905281517f3914ba80eb00486e7a58b91fb4795283df0c5b507eea9cf7c77cce26cc70d25c929181900390910190a1600190920191610411565b6006541561050157fe5b6040805185815290517fb65ebb6b17695b3a5612c7a0f6f60e649c02ba24b36b546b8d037e98215fdb8d9181900360200190a150505050565b60025481565b60075460ff16151561055157600080fd5b60035481101561056057600080fd5b61056933610366565b156105fb57604080517f08c379a000000000000000000000000000000000000000000000000000000000815260206004820152602a60248201527f706c65617365206e6f742075736520636f6e74726163742063616c6c2074686960448201527f732066756e6374696f6e00000000000000000000000000000000000000000000606482015290519081900360840190fd5b61060c60043363ffffffff61090516565b1561061657600080fd5b60025434101561062557600080fd5b33600090815260086020526040902054610645903463ffffffff610a6a16565b336000818152600860205260409020918255426001909201919091556106739060049063ffffffff610a8016565b5033600081815260086020908152604091829020805460019091015483519485529184015282820152517fbca387acb0ba7d06e329c4372885bb664f19a98153ccf3e74e56c136bf0e88c49181900360600190a150565b6008602052600090815260409020805460019091015482565b600054600160a060020a031633146106fa57600080fd5b600355565b6006545b90565b60606107126004610b0f565b905090565b61072860043363ffffffff61090516565b151561073357600080fd5b6001805433600090815260086020526040902090910154429101111561075857600080fd5b3360008181526008602052604080822054905181156108fc0292818181858888f1935050505015801561078f573d6000803e3d6000fd5b50336000818152600860205260408120556107b29060049063ffffffff61092416565b506040805133815290517f03c628a4c93ed860bebcdb8d45ac895f4e4b31b42deea215750fdac0403d66dd9181900360200190a1565b600054600160a060020a031633146107ff57600080fd5b6007805460ff19169055565b60035481565b60015481565b60008054600160a060020a0316331461082f57600080fd5b61084060048363ffffffff61090516565b151561084b57600080fd5b50600160a060020a03811660008181526008602052604080822054905190929183156108fc02918491818181858888f19350505050158015610891573d6000803e3d6000fd5b50600160a060020a0382166000908152600860205260408120556108bc60048363ffffffff61092416565b5060408051600160a060020a03841681526020810183905281517f3914ba80eb00486e7a58b91fb4795283df0c5b507eea9cf7c77cce26cc70d25c929181900390910190a15050565b600160a060020a03166000908152602091909152604090205460ff1690565b600160a060020a03811660009081526020839052604081205481908190819060ff1615156109555760009350610a61565b600160a060020a038516600090815260208781526040808320805460ff1916905560028901805460018b019093529220549094509250600019840184811061099957fe5b600091825260209091200154600287018054600160a060020a0390921692508291849081106109c457fe5b6000918252602080832091909101805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a03948516179055918316815260018801909152604090208290556002860180546000198501908110610a2057fe5b6000918252602090912001805473ffffffffffffffffffffffffffffffffffffffff1916905560028601805490610a5b906000198301610b75565b50600193505b50505092915050565b600082820183811015610a7957fe5b9392505050565b600160a060020a03811660009081526020839052604081205460ff1615610aa9575060006103bd565b50600160a060020a0316600081815260208381526040808320805460ff19166001908117909155600286018054968201845291842086905585810182559083529120909201805473ffffffffffffffffffffffffffffffffffffffff1916909117905590565b606081600201805480602002602001604051908101604052809291908181526020018280548015610b6957602002820191906000526020600020905b8154600160a060020a03168152600190910190602001808311610b4b575b50505050509050919050565b815481835581811115610b9957600083815260209020610b99918101908301610b9e565b505050565b61070391905b80821115610bb85760008155600101610ba4565b50905600a165627a7a72305820a9f9d3ac219ec6ce3b24845fac5517ccd5313ee5d15b0581dfd38d69ef8a50990029'

contract = cf.cpc.contract(abi=abi, bytecode=binary)

instance = cf.cpc.contract(abi=abi, address=address)


def save(member):
    cnt = Congress.objects.filter(address=member).count()
    if cnt == 0:
        log.info(f'add new member {member}')
        obj = Congress(address=member)
        obj.save()
    else:
        log.info(f'already exist member {member}')

def sync():
    # get congress's members from contracts
    log.info('sync from contract')
    num = instance.functions.getCongressNum().call()
    
    log.info(f'num of congress is {num}')

    members = instance.functions.getCongress().call()
    # add members to the table
    for member in members:
        save(member)
    # cleanup table, remove those not in members
    for exist in Congress.objects.all():
        if exist.address not in members:
            log.info(f'remove member {exist.address}')
            exist.delete()

def main():
    sync()


if __name__ == '__main__':
    main()
