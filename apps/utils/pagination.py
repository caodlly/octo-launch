from rest_framework.pagination import LimitOffsetPagination


class SmallResultsSetPagination(LimitOffsetPagination):
    max_limit = 50
