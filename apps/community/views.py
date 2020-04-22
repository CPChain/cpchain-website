
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from decimal import Decimal
from cpc_fusion import Web3

from django_filters.rest_framework import DjangoFilterBackend

from .models import Task, Proposal, Congress, ApprovedAddress, VotedAddress, ProposalType, TaskClaim
from .serializers import TasksSerializer, ProposalsSerializer, ApprovedAddressSerializer, \
    VotedAddressAddressSerializer, ProposalsCreateSerializer, \
    CongressSerializer, ProposalTypeSerializer, TaskClaimSerializer
from .permissions import IPLimitPermission

from cpchain_test.config import cfg

# web3
host = cfg["chain"]["ip"]
port = cfg["chain"]["port"]

cf = Web3(Web3.HTTPProvider(f'http://{host}:{port}'))

# congress contract
congressAddress = cfg['community']['congress']
congressABI = cfg['community']['congressABI'][1:-1].replace('\\', '')
congressInstance = cf.cpc.contract(abi=congressABI, address=congressAddress)

# proposal contract
proposalAddress = cfg['community']['proposal']
proposalABI = cfg['community']['proposalABI'][1:-1].replace('\\', '')
proposalInstance = cf.cpc.contract(abi=proposalABI, address=proposalAddress)

class ConfigViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    合约参数

    + `period` 和 `maxPeriod` 单位为秒
    + `amountThreshold` 单位为 `cpc`
    + `approvalThreshold` 表示赞同个数
    + `voteThreshold` 表示比例
    + `congressThreshold` 单位为 `cpc`
    """
    queryset = Task.objects.all()
    serializer_class = TasksSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        return Response({
            "proposal": {
                "amountThreshold": Decimal(proposalInstance.functions.amountThreshold().call()) / Decimal(1e18),
                "approvalThreshold": proposalInstance.functions.approvalThreshold().call(),
                "voteThreshold": proposalInstance.functions.voteThreshold().call()/100,
                "maxPeriod": proposalInstance.functions.maxPeriod().call(),
                "idLength": proposalInstance.functions.idLength().call(),
            },
            "congress": {
                "period": congressInstance.functions.period().call(),
                "congressThreshold": Decimal(congressInstance.functions.congressThreshold().call()) / Decimal(1e18 + 0.1),
                "supportedVersion": congressInstance.functions.supportedVersion().call(),
            }
        })


class ContractViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    合约地址及合约 ABI
    """
    queryset = Task.objects.all()
    serializer_class = TasksSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        proposal_addr = cfg['community']['proposal']
        congress_addr = cfg['community']['congress']

        proposal_abi = cfg['community']['proposalABI'][1:-1].replace('\\', '')
        congress_abi = cfg['community']['congressABI'][1:-1].replace('\\', '')

        proposal_version = cfg['community']['proposalVersion']
        congress_version = cfg['community']['congressVersion']

        return Response({
            "proposal": {
                'address': proposal_addr,
                'abi': proposal_abi,
                'version': proposal_version,
            },
            "congress": {
                'address': congress_addr,
                'abi': congress_abi,
                'version': congress_version,
            }
        })


class TaskClaimViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """
    任务认领接口
    """

    queryset = TaskClaim.objects.all()
    serializer_class = TaskClaimSerializer
    permission_classes = [IPLimitPermission]


class TasksViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    任务
    """
    queryset = Task.objects.all()
    serializer_class = TasksSerializer


class ProposalTypeViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    提案类型
    """
    queryset = ProposalType.objects.all()
    serializer_class = ProposalTypeSerializer


class ProposalsViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """
    Proposals
    """
    queryset = Proposal.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    permission_classes = [IPLimitPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return ProposalsCreateSerializer
        return ProposalsSerializer

    @action(detail=False, methods=['get'])
    def voted(self, request):
        """
        判断地址是否已投票

        + proposal_id: proposal id
        + address: 地址

        返回值

        ```json
        {
            "exists": true/false
        }
        ```
        """
        queryset = VotedAddress.objects.all()
        proposal_id = self.request.query_params.get('proposal_id')
        address = self.request.query_params.get('address')
        cnt = 0
        if address:
            cnt = self.queryset.filter(
                proposal_id=proposal_id, address=address).count()
        return Response({"exists": cnt > 0})

    @action(detail=False, methods=['get'])
    def liked(self, request):
        """
        判断地址是否已赞同

        + proposal_id: proposal id
        + address: 地址

        返回值

        ```json
        {
            "exists": true/false
        }
        ```
        """
        queryset = ApprovedAddress.objects.all()
        proposal_id = self.request.query_params.get('proposal_id')
        address = self.request.query_params.get('address')
        cnt = 0
        if address:
            cnt = self.queryset.filter(
                proposal_id=proposal_id, address=address).count()
        return Response({"exists": cnt > 0})


class ApprovedAddressViewSet(mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    """
    已赞同地址

    **Parameters**

    * proposal_id -- ID of the proposal

    """
    queryset = ApprovedAddress.objects.all()
    serializer_class = ApprovedAddressSerializer

    def get_queryset(self):
        queryset = ApprovedAddress.objects.all()
        proposal_id = self.request.query_params.get('proposal_id')

        if proposal_id:
            queryset = queryset.filter(proposal_id=proposal_id)
        return queryset


class VotedAddressViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    已投票地址

    **Parameters**

    * proposal_id -- ID of the proposal

    """
    queryset = VotedAddress.objects.all()
    serializer_class = VotedAddressAddressSerializer

    def get_queryset(self):
        queryset = VotedAddress.objects.all()
        proposal_id = self.request.query_params.get('proposal_id')

        if proposal_id:
            queryset = queryset.filter(proposal_id=proposal_id)
        return queryset


class CongressViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Congress
    """

    queryset = Congress.objects.all()
    serializer_class = CongressSerializer

    @action(detail=False, methods=['get'])
    def joined(self, request):
        """
        判断地址是在议会中

        + address: 地址

        返回值

        ```json
        {
            "exists": true/false
        }
        ```
        """
        queryset = Congress.objects.all()
        address = self.request.query_params.get('address')
        cnt = 0
        if address:
            cnt = self.queryset.filter(address=address).count()
        return Response({"exists": cnt > 0})
