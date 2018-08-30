from django.db import models
from django.db.models import Q, Sum


class TokenOrdersQuerySet(models.query.QuerySet):
    def token_orders(self, **kwargs):
        _filter_list = {
            'customer_external_id__exact': kwargs['customer_external_id'],
        }

        if 'token_order_external_id' in kwargs:
            _filter_list.update(token_order_external_id__exact=kwargs['token_order_external_id'])

        if 'txn_id' in kwargs:
            _filter_list.update(txn_id__exact=kwargs['txn_id'])

        return self.filter(**_filter_list)

    def order_from_txn(self, **kwargs):
        _filter_list = {
            'txn_id__exact': kwargs['txn_id'],
        }

        return self.filter(**_filter_list)

    def completed(self):
        return self.filter(Q(payment_received=True) | Q(tokens_credited=True))

    def pending(self):
        return self.filter((Q(payment_status__isnull=True) | Q(payment_status__gte=0)) &
                           (Q(payment_received=False) | Q(tokens_credited=False)))

    def cancelled(self):
        return self.filter(Q(payment_status__lt=0))

    def stats(self):
        return self.aggregate(usd_value=Sum('usd_value'))
