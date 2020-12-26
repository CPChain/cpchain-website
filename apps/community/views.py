
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, BaseFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from decimal import Decimal
from cpc_fusion import Web3

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import compat
from django.db.models import Q

import warnings

from .models import Task, Proposal, Congress, ApprovedAddress, VotedAddress, ProposalType, TaskClaim, Email, ClaimEmailReceiver
from .serializers import TasksSerializer, ProposalsSerializer, ApprovedAddressSerializer, \
    VotedAddressAddressSerializer, ProposalsCreateSerializer, \
    CongressSerializer, ProposalTypeSerializer, TaskClaimSerializer, EmailSerializer
from .permissions import IPLimitPermission

from cpchain_test.config import cfg

from log import get_log

log = get_log('app')

# web3
host = cfg["chain"]["ip"]
port = cfg["chain"]["port"]

cf = Web3(Web3.HTTPProvider(f'http://{host}:{port}'))

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
        # congress contract
        congressAddress = cfg['community']['congress']
        congressABI = cfg['community']['congressABI'][1:-1].replace('\\', '')
        congressInstance = cf.cpc.contract(abi=congressABI, address=congressAddress)

        # proposal contract
        proposalAddress = cfg['community']['proposal']
        proposalABI = cfg['community']['proposalABI'][1:-1].replace('\\', '')
        proposalInstance = cf.cpc.contract(abi=proposalABI, address=proposalAddress)
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
    permission_classes = [IsAuthenticated, IPLimitPermission]

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        try:
            if res.status_code == 201:
                log.info('there is a claim for task')
                for item in ClaimEmailReceiver.objects.filter():
                    log.debug(f'name: {item.name}, email: {item.email}')
                    # get the title of task
                    task_id = request.data['task_id']
                    task = Task.objects.get(id=task_id)
                    if not task:
                        log.error(f"not exists task {task_id}")
                        continue
                    # content
                    content = f'''
                    <div>
                        <ul>
                            <li>Task Title: <label>{task.title}</label></li>
                            <li>Email: <label>{request.data["email"]}</label></li>
                            <li>Name: <label>{request.data["name"]}</label></li>
                            <li>Adantages: <label>{request.data["advantages"]}</label></li>
                            <li>Estimated Date: <label>{request.data["estimated_date"]}</label></li>
                        </ul>
                    </div>
                    '''
                    log.debug(content)

                    # create email
                    serializer = EmailSerializer(data=dict(content=content, to=item.email))
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
        except Exception as e:
            log.error(e)
        return res


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

class StatusFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, qs, view):
        status = request.query_params.get('status')
        client_id = request.query_params.get('client_id')
        if status:
            labels = status.split(',')
            filters = Q(status__in=labels)
            if 'submitted' in labels and client_id:
                filters |= Q(status='unchecked') & Q(client_id=client_id)
            qs = qs.filter(filters)
        elif request.parser_context['kwargs'].get('pk') == None:
            if not client_id:
                qs = qs.filter(~Q(status="unchecked"))
            else:
                qs = qs.filter(~Q(status="unchecked")|Q(status='unchecked') & Q(client_id=client_id))
        return qs

    def get_schema_fields(self, view):
        return [
            compat.coreapi.Field(
                name='status',
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="e.g.: submitted,deposited"
                )
            ),
            compat.coreapi.Field(
                name='client_id',
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="client_id"
                )
            )
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'status',
                'required': False,
                'in': 'query',
                'description': 'status of proposal',
                'schema': {
                    'type': 'string',
                },
            },
            {
                'name': 'client_id',
                'required': False,
                'in': 'query',
                'description': 'client_id of client',
                'schema': {
                    'type': 'string',
                },
            }
        ]

class ProposalsViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """
    Proposals

    Filters
    ---
    + status，e.g. `status=submitted,deposited`
    + client_id

    Ordering
    ---
    + updated_at
    + status

    *reverse: -updated_at*

    """
    queryset = Proposal.objects.all()
    filter_backends = [StatusFilterBackend, OrderingFilter]
    ordering_fields = ["updated_at", "status"]
    ordering = "-updated_at"
    filter_fields = ['status', 'client_id']
    permission_classes = [IsAuthenticated, IPLimitPermission]
    

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
