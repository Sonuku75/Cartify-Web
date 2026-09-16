"""Standard pagination classes for Cartify REST APIs."""
from typing import Any, List
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination configured with 20 items per page by default.
    Wraps paginated output into the standardized Cartify success envelope:
    {
        "success": true,
        "message": "Request successful",
        "data": {
            "count": 100,
            "next": "...",
            "previous": null,
            "results": [...]
        }
    }
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data: List[Any]) -> Response:
        return Response({
            "success": True,
            "message": "Request successful",
            "data": {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            },
        })
