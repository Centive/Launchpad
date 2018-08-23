from django.db import models


class UserProfileQuerySet(models.query.QuerySet):
    def basic_profile(self, **kwargs):
        _filter_list = {
            'user': kwargs['user_id'],
        }

        return self.filter(**_filter_list)
