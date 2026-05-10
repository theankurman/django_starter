from typing import cast, TypedDict

from django import template
from django.http import HttpRequest
from django.core.paginator import Page

register = template.Library()


class _TLink(TypedDict):
    label: str
    link: str | None
    is_active: bool


@register.inclusion_tag("core/partials/pagination/pagination.html", takes_context=True)
def paginate(
    context: dict,
    page_obj: Page | None = None,
    item_name: str = "items",
    on_each_side: int = 1,
    on_ends: int = 2,
):
    request: HttpRequest = context["request"]

    page_obj = page_obj or cast(Page | None, context.get("page_obj"))
    if not page_obj:
        return {}

    def _get_page_link(page_number: int | str):
        params = request.GET.copy()
        params["page"] = str(page_number)
        link = request.path_info + "?" + params.urlencode()
        return link

    paginator = page_obj.paginator
    num_pages = paginator.num_pages
    page_number = page_obj.number

    # link: {label:str, link:str}
    links: list[_TLink] = []

    # start
    for pn in range(1, on_ends + 1):
        if pn < page_number:
            links.append(
                {"label": str(pn), "link": _get_page_link(pn), "is_active": False}
            )

    # ellipses
    if page_number - on_each_side - on_ends > 1:
        links.append({"label": "...", "link": None, "is_active": False})

    # before
    for pn in range(page_number - on_each_side, page_number + 1):
        if pn > on_ends and pn < page_number:
            links.append(
                {"label": str(pn), "link": _get_page_link(pn), "is_active": False}
            )

    # current page
    links.append({"label": str(page_number), "link": None, "is_active": True})

    # after
    for pn in range(page_number + 1, page_number + on_each_side + 1):
        if pn < num_pages:
            links.append(
                {"label": str(pn), "link": _get_page_link(pn), "is_active": False}
            )

    # ellipses
    if (num_pages - on_ends) - (page_number + on_each_side) > 1:
        links.append({"label": "...", "link": None, "is_active": False})

    # end
    # after
    for pn in range(num_pages - on_ends, num_pages + 1):
        if pn > page_number + on_each_side and pn < num_pages:
            links.append(
                {"label": str(pn), "link": _get_page_link(pn), "is_active": False}
            )

    return {
        "links": links,
        "start_index": page_obj.start_index(),
        "end_index": page_obj.end_index(),
        "total": paginator.count,
        "item_name": item_name,
    }
