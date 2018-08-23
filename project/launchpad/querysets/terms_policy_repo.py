from django.db import models


class TermsPolicyRepoQuerySet(models.query.QuerySet):
    def latest_term(self, **kwargs):
        _filter_list = {
            'term_status__exact': 'valid',
            'term_type__exact': kwargs['term_type'],
        }

        return self.filter(**_filter_list).order_by('-term_id').all()[:1]

    def terms(self, **kwargs):
        _filter_list = {
            'term_status__exact': 'valid',
            'term_type__exact': kwargs['term_type'],
        }

        if 'term_version' in kwargs:
            _filter_list.update(term_version__exact=kwargs['term_version'])

        return self.filter(**_filter_list)
