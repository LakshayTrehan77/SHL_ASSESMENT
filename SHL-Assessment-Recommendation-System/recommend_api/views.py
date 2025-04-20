from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny  # <--- add this

from .serializers import QueryRequestSerializer, RecommendationsResponseSerializer
from .authentication import APIKeyAuthentication  # keep if you're using it
from rag_engine import get_rag_chain

rag_chain = get_rag_chain()

def map_doc_to_assessment(doc):
    meta = getattr(doc, 'metadata', {}) or {}
    return {
        'url':               meta.get('url', ''),
        'adaptive_support':  'Yes' if meta.get('adaptive_support', False) else 'No',
        'description':       meta.get('description', ''),
        'duration':          int(meta.get('duration', 0)),
        'remote_support':    'Yes' if meta.get('remote_support', False) else 'No',
        'test_type':         meta.get('test_type', []),
    }

class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'status': 'healthy'}, status=status.HTTP_200_OK)


class RecommendView(APIView):
    # Use this if you're testing without auth:
    permission_classes = [AllowAny]
    authentication_classes = []  # comment this out if you want to use APIKeyAuthentication

    # Uncomment below if you want to use authentication:
    # authentication_classes = [APIKeyAuthentication]

    def post(self, request):
        serializer = QueryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data['query'].strip()

        docs = rag_chain.retriever.get_relevant_documents(query)
        if not docs:
            return Response(
                {'detail': 'No assessments found for the given query.'},
                status=status.HTTP_404_NOT_FOUND
            )

        assessments = [map_doc_to_assessment(d) for d in docs[:10]]
        response = {'recommended_assessments': assessments}
        return Response(
            RecommendationsResponseSerializer(response).data,
            status=status.HTTP_200_OK
        )
