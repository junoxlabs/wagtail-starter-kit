from django.shortcuts import render
from django.core.paginator import Paginator
from wagtail.models import Page
from wagtail.contrib.search_promotions.models import Query


def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)
        
        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    search_results = paginator.get_page(page)

    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })

