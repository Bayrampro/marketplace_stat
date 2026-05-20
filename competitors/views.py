from django.shortcuts import render

from .forms import CompetitorSearchForm
from .services import search_competitors


def index(request):
    form = CompetitorSearchForm(request.GET or None)
    products = []
    has_searched = False

    if request.GET:
        has_searched = True
        if form.is_valid():
            products = search_competitors(form.cleaned_data["query"])
    no_results = has_searched and form.is_valid() and not products

    return render(
        request,
        "competitors/index.html",
        {
            "active_tab": "competitors",
            "form": form,
            "products": products,
            "has_searched": has_searched,
            "no_results": no_results,
        },
    )
