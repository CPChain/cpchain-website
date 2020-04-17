
from rest_framework import serializers

from .models import Task, Proposal, ApprovedAddress, VotedAddress, Congress, ProposalType

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ProposalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'

class ProposalsCreateSerializer(serializers.ModelSerializer):

    proposal_id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Proposal
        fields = ['proposal_id', 'title', 'proposal_type', 'description', 'proposer_addr']

class ApprovedAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovedAddress
        fields = '__all__'

class VotedAddressAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotedAddress
        fields = '__all__'

class CongressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Congress
        fields = '__all__'

class ProposalTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProposalType
        fields = '__all__'
