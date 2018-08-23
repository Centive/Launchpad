from django.db import models


class UserEligibilityRegistryQuerySet(models.query.QuerySet):
    def last_consent(self, **kwargs):
        _filter_list = {
            'customer_external_id__exact': kwargs['external_id'],
        }

        return self.filter(**_filter_list).order_by('-user_eligibility_id').all()[:1]
