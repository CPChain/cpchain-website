
from rest_framework import serializers

from .models import Tasks, Proposals, ApprovedAddress, VotedAddress, Congress, ProposalType

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'

class ProposalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposals
        fields = '__all__'

class ProposalsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposals
        fields = ['title', 'proposal_type', 'description', 'proposer_addr']

class ProposalsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposals
        fields = ['title', 'proposal_type', 'description', 'status', 'reason']

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
