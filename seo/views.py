from django.shortcuts import render

from .forms import SEORequestForm
from .services import generate_seo_description


def index(request):
    generated_request = None

    if request.method == "POST":
        form = SEORequestForm(request.POST)
        if form.is_valid():
            generated_text = generate_seo_description(
                product_name=form.cleaned_data["product_name"],
                category=form.cleaned_data["category"],
                keywords=form.cleaned_data["keywords"],
                advantages=form.cleaned_data["advantages"],
            )
            generated_request = form.save(commit=False)
            generated_request.generated_text = generated_text
            generated_request.save()
    else:
        form = SEORequestForm()

    return render(
        request,
        "seo/index.html",
        {
            "active_tab": "seo",
            "form": form,
            "generated_request": generated_request,
        },
    )
