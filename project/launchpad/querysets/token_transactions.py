from django.db import models
from django.db.models import Sum


class TokenTransactionsQuerySet(models.query.QuerySet):
    def token_transactions(self, **kwargs):
        _filter_list = {
            'customer_external_id__exact': kwargs['customer_external_id'],
        }

        if 'token_transaction_external_id' in kwargs:
            _filter_list.update(token_transaction_external_id__exact=kwargs['token_transaction_external_id'])

        return self.filter(**_filter_list)

    def total_holdings(self):
        return self.aggregate(Sum('token_value'))
