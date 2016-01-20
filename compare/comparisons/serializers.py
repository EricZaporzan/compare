from rest_framework import serializers

from .models import ComparisonItemVote


class ComparisonItemVoteSerializer(serializers.Serializer):
    date_created = serializers.DateTimeField(read_only=True)
