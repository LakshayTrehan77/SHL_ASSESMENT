from rest_framework import serializers

class QueryRequestSerializer(serializers.Serializer):
    query = serializers.CharField()

class AssessmentSerializer(serializers.Serializer):
    url = serializers.URLField()
    adaptive_support = serializers.ChoiceField(choices=["Yes", "No"])
    description = serializers.CharField()
    duration = serializers.IntegerField()
    remote_support = serializers.ChoiceField(choices=["Yes", "No"])
    test_type = serializers.ListField(child=serializers.CharField())

class RecommendationsResponseSerializer(serializers.Serializer):
    recommended_assessments = AssessmentSerializer(many=True)
