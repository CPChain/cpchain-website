
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from .models import Tasks, Proposals, Congress, ApprovedAddress, VotedAddress
from .serializers import TasksSerializer, ProposalsSerializer, ApprovedAddressSerializer, \
    VotedAddressAddressSerializer, ProposalsCreateSerializer, ProposalsUpdateSerializer, \
    CongressSerializer


class TasksViewSet(viewsets.ModelViewSet):
    """
    任务
    """
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer


class ProposalsViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    Proposals
    """
    queryset = Proposals.objects.all()
    serializer_class = ProposalsSerializer


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


class ProposalsUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):

    """
    Proposals

    用于决策议会改变提案
    """

    queryset = Proposals.objects.all()
    serializer_class = ProposalsUpdateSerializer


class ProposalsCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    """
    Proposals

    用户在前台提交提案
    """

    queryset = Proposals.objects.all()
    serializer_class = ProposalsCreateSerializer


class CongressViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Congress
    """

    queryset = Congress.objects.all()
    serializer_class = CongressSerializer
