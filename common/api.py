from rest_framework.pagination import PageNumberPagination


# create pagination class that can return
# 1. the total number of pages
# 2. the current page
# 3. put result in a data key


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        response = super(CustomPagination, self).get_paginated_response(data)
        response.data["total_pages"] = self.page.paginator.num_pages
        response.data["current_page"] = self.page.number
        response.data["data"] = response.data["results"]
        response.data.pop("results")
        # remove next and previous keys
        response.data.pop("next")
        response.data.pop("previous")
        return response