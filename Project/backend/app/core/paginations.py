from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class SmallResultSetPagination(PageNumberPagination):
    page_size = 20
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(
            {
                'current_page': self.page.number,
                'count': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'results': data,
            }
        )
