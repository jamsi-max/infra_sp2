from django_filters import FilterSet, CharFilter
from rest_framework import filters
from reviews.models import Title


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get("genre"):
            return ["genre__slug"]
        return super().get_search_fields(view, request)


class TitleFilter(FilterSet):
    genre = CharFilter(field_name="genre__slug")
    category = CharFilter(field_name="category__slug")
    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Title
        fields = ["category", "year", "genre", "name"]
