
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Task, Proposal, Congress, ApprovedAddress, VotedAddress, ProposalType, TaskClaim
from .serializers import TasksSerializer, ProposalsSerializer, ApprovedAddressSerializer, \
    VotedAddressAddressSerializer, ProposalsCreateSerializer, \
    CongressSerializer, ProposalTypeSerializer, TaskClaimSerializer

from cpchain_test.config import cfg


class ContractViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    合约地址及合约 ABI
    """
    queryset = Task.objects.all()
    serializer_class = TasksSerializer

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
    # serializer_class = ProposalsSerializer

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
