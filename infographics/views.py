import mimetypes

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render

from .forms import InfographicForm
from .models import InfographicRequest
from .services import generate_infographic


def index(request):
    generated_request = None

    if request.method == "POST":
        form = InfographicForm(request.POST, request.FILES)
        if form.is_valid():
            generated_request = InfographicRequest.objects.create(
                original_image=form.cleaned_data["image"],
                title=form.cleaned_data["title"],
                keywords=form.cleaned_data["keywords"],
                layout_type="processing",
            )
            generated_path, layout_type = generate_infographic(
                generated_request.original_image.path,
                generated_request.title,
                generated_request.keywords,
            )
            generated_request.generated_image.name = generated_path
            generated_request.layout_type = layout_type
            generated_request.save(update_fields=["generated_image", "layout_type"])
    else:
        form = InfographicForm()

    return render(
        request,
        "infographics/index.html",
        {
            "active_tab": "infographics",
            "form": form,
            "generated_request": generated_request,
        },
    )


def download(request, pk):
    infographic = get_object_or_404(InfographicRequest, pk=pk)
    if not infographic.generated_image:
        raise Http404("Generated image was not found.")

    content_type, _ = mimetypes.guess_type(infographic.generated_image.name)
    extension = infographic.generated_image.name.rsplit(".", 1)[-1]
    return FileResponse(
        open(infographic.generated_image.path, "rb"),
        as_attachment=True,
        filename=f"generated_product_image.{extension}",
        content_type=content_type or "application/octet-stream",
    )
