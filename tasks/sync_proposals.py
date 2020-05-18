"""

sync all proposals from proposal contract

"""

import sys
sys.path.append("..")

from cpc_fusion import Web3
from datetime import datetime as dt
from cpchain_test.config import cfg
import django
import logging
import os
import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cpchain_test.settings')
django.setup()

# import models
from community.models import Proposal, ApprovedAddress, VotedAddress

from log import get_log

STATUS = {
    0: 'deposited',
    1: 'community congress',
    2: 'decision congress',
    3: 'timeout'
}

log = get_log('sync-proposals')

host = cfg["chain"]["ip"]
port = cfg["chain"]["port"]
address = cfg['community']['proposal']

log.info(f"chain rpc interface: http://{host}:{port}")
log.info(f'congress constract\'s address is {address}')

cf = Web3(Web3.HTTPProvider(f'http://{host}:{port}'))

# ProposalABI is the input ABI used to generate the binding from.
# abi = "[{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"getLockedTime\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"getStatus\",\"outputs\":[{\"name\":\"\",\"type\":\"uint8\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"enabled\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"getLockedAmount\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"withdraw\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"getPeriod\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"length\",\"type\":\"uint16\"}],\"name\":\"setIDLength\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"checkTimeout\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"enableContract\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"threshold\",\"type\":\"uint256\"}],\"name\":\"setAmountThreshold\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"refundAll\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"threshold\",\"type\":\"uint16\"}],\"name\":\"setVoteThreshold\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"maxPeriod\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"getOwner\",\"outputs\":[{\"name\":\"\",\"type\":\"address\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"getApprovalCnt\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"approval\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"voteThreshold\",\"outputs\":[{\"name\":\"\",\"type\":\"uint16\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"getVotedAddress\",\"outputs\":[{\"name\":\"\",\"type\":\"address[]\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"getCongressNum\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"getApprovedAddress\",\"outputs\":[{\"name\":\"\",\"type\":\"address[]\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"approvalThreshold\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"name\":\"proposalsIDList\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"congress\",\"outputs\":[{\"name\":\"\",\"type\":\"address\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"disableContract\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"amountThreshold\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"idLength\",\"outputs\":[{\"name\":\"\",\"type\":\"uint16\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"threshold\",\"type\":\"uint256\"}],\"name\":\"setApprovalThreshold\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"period\",\"type\":\"uint256\"}],\"name\":\"setMaxPeriod\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"getProposalsCnt\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"},{\"name\":\"period\",\"type\":\"uint256\"}],\"name\":\"submit\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"getVoteCnt\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"vote\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"id\",\"type\":\"string\"}],\"name\":\"refund\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"inputs\":[{\"name\":\"_congressAddr\",\"type\":\"address\"}],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"who\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"id\",\"type\":\"string\"},{\"indexed\":false,\"name\":\"period\",\"type\":\"uint256\"},{\"indexed\":false,\"name\":\"lockedAmount\",\"type\":\"uint256\"},{\"indexed\":false,\"name\":\"lockedTime\",\"type\":\"uint256\"}],\"name\":\"SubmitProposal\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"who\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"id\",\"type\":\"string\"}],\"name\":\"ApprovalProposal\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"who\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"id\",\"type\":\"string\"}],\"name\":\"VoteProposal\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"who\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"id\",\"type\":\"string\"}],\"name\":\"WithdrawMoney\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"id\",\"type\":\"string\"}],\"name\":\"proposalTimeout\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"name\":\"id\",\"type\":\"string\"}],\"name\":\"ownerRefund\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[],\"name\":\"ownerRefundAll\",\"type\":\"event\"}]"
abi = cfg['community']['proposalABI'][1:-1].replace('\\', '')
instance = cf.cpc.contract(abi=abi, address=address)

def sync_proposals():
    
    cnt = instance.functions.getProposalsCnt().call()
    log.info(f"proposal's count is {cnt}")
    # iterate
    for i in range(cnt):
        try:
            proposal = instance.call().proposalsIDList(i)
            log.info(f'get proposal - {proposal}')
            origin = None
            # check if the proposal exists in table
            if Proposal.objects.filter(proposal_id=proposal).count() == 0:
                # if not exists
                log.info(f"add new proposal - {proposal}")
                obj = Proposal(proposal_id=proposal)
                obj.save()
            else:
                origin = Proposal.objects.filter(proposal_id=proposal)[0]

            obj = Proposal.objects.filter(proposal_id=proposal)[0]
            # sync status
            status = instance.functions.getStatus(proposal).call()
            status = STATUS[status]
            log.debug(f'status of {proposal} is {status}')
            obj.status = status

            # sync period
            period = instance.functions.getPeriod(proposal).call()
            log.debug(f'period of {proposal} is {period}')
            obj.period = period

            # sync lockedAmount
            amount = instance.functions.getLockedAmount(proposal).call()
            log.debug(f'amount of {proposal} is {amount}')
            obj.locked_amount = amount

            # sync lockedTime
            locked_time = instance.functions.getLockedTime(proposal).call()
            log.debug(f'locked-time of {proposal} is {locked_time}')
            obj.locked_time = dt.fromtimestamp(locked_time, tz=pytz.timezone('Asia/Shanghai'))

            # sync owner
            owner = instance.functions.getOwner(proposal).call()
            log.debug(f'owner of {proposal} is {owner}')
            obj.depositor_addr = owner

            # sync approvted cnt
            likes = instance.functions.getApprovalCnt(proposal).call()
            log.debug(f'likes of {proposal} is {likes}')
            obj.likes = likes

            # sync approved address
            approved = instance.functions.getApprovedAddress(proposal).call()
            for addr in approved:
                if ApprovedAddress.objects.filter(proposal_id=proposal, address=addr).count() == 0:
                    log.debug(f'add approved address {addr} for {proposal}')
                    item = ApprovedAddress(proposal_id=proposal, address=addr)
                    item.save()


            # sync voted cnt
            votes = instance.functions.getVoteCnt(proposal).call()
            log.debug(f'votes of {proposal} is {votes}')
            obj.votes = votes

            # sync voted address
            voted = instance.functions.getVotedAddress(proposal).call()
            for addr in voted:
                if VotedAddress.objects.filter(proposal_id=proposal, address=addr).count() == 0:
                    log.debug(f'add voted address {addr} for {proposal}')
                    item = VotedAddress(proposal_id=proposal, address=addr)
                    item.save()

            if origin != None:
                # validate changes, update if have changes
                validators = [
                    lambda origin, obj: origin.status != obj.status,
                    lambda origin, obj: origin.locked_amount != obj.locked_amount,
                    lambda origin, obj: origin.likes != obj.likes,
                    lambda origin, obj: origin.votes != obj.votes,
                ]
                for v in validators:
                    if v(origin, obj):
                        obj.save()
                        break
            else:
                obj.save()
        except Exception as e:
            log.error(e)
        

if __name__ == '__main__':
    sync_proposals()
