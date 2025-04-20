from django.shortcuts import render
import requests
import json

def recommendation_view(request):
    error = None
    assessments = []
    query = request.POST.get('query', '') if request.method == 'POST' else ''
    page = request.GET.get('page', 1)  # Default to page 1

    if request.method == 'POST' and query:
        try:
            res = requests.post(
                "http://localhost:8000/recommend",
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )
            res.raise_for_status()
            data = res.json()
            assessments = data.get("recommended_assessments", [])

            if not assessments:
                error = "No recommendations found."
            else:
                for a in assessments:
                    a['name'] = a.get('description', 'No description')[:50] + '...' if len(a.get('description', '')) > 50 else a.get('description', '')
                    a['test_type_str'] = ', '.join(a.get('test_type', [])) if a.get('test_type') else 'N/A'
        except requests.exceptions.HTTPError as e:
            error = f"HTTP error occurred: {e}"
        except requests.exceptions.RequestException as e:
            error = f"Network error occurred: {e}"
        except ValueError as e:
            error = f"Invalid response format: {e}"
        except Exception as e:
            error = f"An error occurred: {e}"

    # Pagination logic (assuming 5 items per page)
    per_page = 100
    total_items = len(assessments)
    total_pages = (total_items + per_page - 1) // per_page
    page = max(1, min(int(page), total_pages))  # Ensure page is within valid range
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_assessments = assessments[start_idx:end_idx]

    return render(request, 'rag_api/recommendation.html', {
        'query': query,
        'error': error,
        'assessments': paginated_assessments,
        'page': page,
        'total_pages': total_pages
    })