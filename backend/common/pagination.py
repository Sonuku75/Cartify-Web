"""Standard pagination classes for Cartify REST APIs."""
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination configured with 20 items per page by default."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
