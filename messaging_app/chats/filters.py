import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    from_this_time = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    to_this_time = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')

    username = django_filters.CharFilter(field="user_name", lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['username', 'created_at']