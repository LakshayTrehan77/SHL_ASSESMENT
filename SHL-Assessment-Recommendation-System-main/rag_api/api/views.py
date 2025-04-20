import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from rag_engine import get_rag_chain

rag_chain = get_rag_chain()



from django.http import JsonResponse

def index(request):
    return JsonResponse({
        "message": "Welcome to the RAG API",
        "endpoints": {
            "/health": "GET",
            "/recommend": "POST"
        }
    })
@require_GET
def health(request):
    return JsonResponse({"status": "healthy"})

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json




@require_POST
@csrf_exempt
def recommend(request):
    try:
        data = json.loads(request.body)
        query = data.get("query", "")
        print(f"Received query: {query}")  # Debug: Log the query
        rag_chain.invoke(query)  # Process the query
        recommended_assessments = rag_chain.retriever.invoke(query)  # Use invoke instead of get_relevant_documents
        print(f"Retrieved documents: {recommended_assessments}")  # Debug: Log the results
        
        # Check if any documents were found
        if not recommended_assessments:
            return JsonResponse({"error": "No assessments found for the query"}, status=404)
        
        # Serialize all documents into the required format
        serialized_assessments = [
            {
                "url": doc.metadata.get("url", ""),
                "adaptive_support": doc.metadata.get("adaptive_support", "No"),
                "description": doc.page_content,  # Use page_content as description
                "duration": doc.metadata.get("duration", 0),
                "remote_support": doc.metadata.get("remote_support", "No"),
                "test_type": doc.metadata.get("test_type", [])
            }
            for doc in recommended_assessments
        ]
        
        return JsonResponse({
            "recommended_assessments": serialized_assessments
        }, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        print(f"Error in recommendation: {str(e)}")  
        return JsonResponse({"error": "Error fetching recommendations. Please try again later."}, status=500)