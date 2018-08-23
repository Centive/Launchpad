from django.db import models


class UserTermsRegistryQuerySet(models.query.QuerySet):
    def last_consent(self, **kwargs):
        _filter_list = {
            'customer_external_id__exact': kwargs['external_id'],
            'term__term_status__exact': 'valid',
            'term__term_type__exact': kwargs['term_type'],
        }

        return self.filter(**_filter_list).order_by('-user_term_id').all()[:1]
