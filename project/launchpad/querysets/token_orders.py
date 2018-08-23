from django.db import models
from django.db.models import Q


class TokenOrdersQuerySet(models.query.QuerySet):
    def token_orders(self, **kwargs):
        _filter_list = {
            'customer_external_id__exact': kwargs['customer_external_id'],
        }

        if 'token_order_external_id' in kwargs:
            _filter_list.update(token_order_external_id__exact=kwargs['token_order_external_id'])

        return self.filter(**_filter_list)

    def pending(self):
        return self.filter(Q(payment_received=False) | Q(tokens_credited=False))
