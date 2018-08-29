from django.db import models

from accounts.models import User
from launchpad.querysets.terms_policy_repo import TermsPolicyRepoQuerySet
from launchpad.querysets.token_orders import TokenOrdersQuerySet
from launchpad.querysets.token_transactions import TokenTransactionsQuerySet
from launchpad.querysets.user_eligibility_registry import UserEligibilityRegistryQuerySet
from launchpad.querysets.user_terms_registry import UserTermsRegistryQuerySet


class TermsPolicyRepo(models.Model):
    term_id = models.BigAutoField(primary_key=True)
    term_type = models.CharField(max_length=50, null=False)
    term_version = models.CharField(max_length=15, null=False)
    term_html = models.TextField(null=False)
    term_text = models.TextField(null=False)
    term_status = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      null=True)

    # Configuration
    #
    objects = TermsPolicyRepoQuerySet.as_manager()

    def __str__(self):
        return '%s - %s - %s' % (self.term_type, self.term_version, self.created_at)


class UserTermsRegistry(models.Model):
    user_term_id = models.BigAutoField(primary_key=True)
    customer_external_id = models.CharField(max_length=64, null=False)
    term = models.ForeignKey(TermsPolicyRepo,
                             db_column='term_id',
                             on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      null=True)

    # Configuration
    #
    objects = UserTermsRegistryQuerySet.as_manager()


class UserEligibilityRegistry(models.Model):
    user_eligibility_id = models.BigAutoField(primary_key=True)
    customer_external_id = models.CharField(max_length=64, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      null=True)

    # Configuration
    #
    objects = UserEligibilityRegistryQuerySet.as_manager()


class TokenOrders(models.Model):
    token_order_id = models.BigAutoField(primary_key=True)
    token_order_external_id = models.CharField(max_length=64, null=False)
    customer_external_id = models.CharField(max_length=64, null=False)
    usd_value = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    token_value = models.DecimalField(max_digits=28, decimal_places=18, null=False)
    payment_currency = models.CharField(max_length=10, null=False)
    payment_currency_value = models.DecimalField(max_digits=28, decimal_places=18, null=True)
    payment_address = models.CharField(max_length=255, null=True)
    payment_destination_tag = models.CharField(max_length=25, null=True)
    txn_id = models.CharField(max_length=255, null=True)
    confirms_needed = models.IntegerField(null=True)
    timeout = models.IntegerField(null=True)
    status_url = models.CharField(max_length=255, null=True)
    qrcode_url = models.CharField(max_length=255, null=True)
    payment_status = models.IntegerField(null=True)
    payment_status_text = models.CharField(max_length=255, null=True)
    payment_received = models.BooleanField(null=False, default=False)
    tokens_credited = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      null=True)

    # Configuration
    #
    objects = TokenOrdersQuerySet.as_manager()

    class Meta:
        ordering = ['-token_order_id']


class TokenTransactions(models.Model):
    token_transaction_id = models.BigAutoField(primary_key=True)
    token_transaction_external_id = models.CharField(max_length=64, null=False)
    customer_external_id = models.CharField(max_length=64, null=False)
    transaction_type = models.CharField(max_length=25, null=False)
    token_value = models.DecimalField(max_digits=28, decimal_places=18, null=False)
    withdrawal_address = models.CharField(max_length=255, null=True)
    txn_id = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      null=True)

    # Configuration
    #
    objects = TokenTransactionsQuerySet.as_manager()

    class Meta:
        ordering = ['-token_transaction_id']


# class SaltEdgeLogins(models.Model):
#     se_login_id = models.BigIntegerField(primary_key=True)
#     se_customer = models.ForeignKey(UserTermsRegistry,
#                                     db_column='se_customer_id',
#                                     on_delete=models.PROTECT)
#     se_login_secret = models.CharField(max_length=64)
#     se_provider = models.ForeignKey(SaltEdgeProviders,
#                                     db_column='se_provider_code',
#                                     to_field='se_provider_code',
#                                     on_delete=models.PROTECT)
#     se_login_status = models.CharField(max_length=32)
#     se_login_data = JSONField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True,
#                                       null=True)
#
#     def __str__(self):
#         return self.se_login_id
#
#
# class SaltEdgeAccounts(models.Model):
#     se_account_id = models.BigIntegerField(primary_key=True)
#     se_account_name = models.CharField(max_length=255)
#     se_login = models.ForeignKey(SaltEdgeLogins,
#                                  db_column='se_login_id',
#                                  on_delete=models.PROTECT)
#     se_account_data = JSONField()
#
#     # Configuration
#     #
#     objects = SaltEdgeAccountsQuerySet.as_manager()
#
#     def __str__(self):
#         return self.se_account_id
#
#
# class SaltEdgeTransactions(models.Model):
#     se_transaction_id = models.BigIntegerField(primary_key=True)
#     se_transaction_amount = models.DecimalField(max_digits=22,
#                                                 decimal_places=2)
#     se_account = models.ForeignKey(SaltEdgeAccounts,
#                                    db_column='se_account_id',
#                                    on_delete=models.PROTECT)
#     se_transaction_data = JSONField()
#
#     # Configuration
#     #
#     objects = SaltEdgeTransactionsQuerySet.as_manager()
#
#     def __str__(self):
#         return self.se_transaction_id
#
#     class Meta:
#         ordering = ['-se_transaction_id']
#
#
# class SourceLogins(models.Model):
#     login_secret = models.CharField(max_length=64,
#                                     unique=True)
#     user_id_external = models.CharField(max_length=64)
#     se_provider = models.ForeignKey(SaltEdgeProviders,
#                                     db_column='se_provider_code',
#                                     to_field='se_provider_code',
#                                     on_delete=models.PROTECT)
#     se_login = models.OneToOneField(SaltEdgeLogins,
#                                     db_column='se_login_id',
#                                     on_delete=models.DO_NOTHING)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True,
#                                       null=True)
#
#     # Configuration
#     #
#     objects = SourceLoginsQuerySet.as_manager()
#
#
# class SourceAccounts(models.Model):
#     account_name = models.CharField(max_length=255)
#     account_nature = models.CharField(max_length=64)
#     currency_code = models.CharField(max_length=3)
#     source_login = models.ForeignKey(SourceLogins,
#                                      db_column='source_login_id',
#                                      on_delete=models.PROTECT)
#     se_account = models.OneToOneField(SaltEdgeAccounts,
#                                       db_column='se_account_id',
#                                       on_delete=models.DO_NOTHING)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True,
#                                       null=True)
#
#     # Configuration
#     #
#     objects = SourceAccountsQuerySet.as_manager()
#
#
# class SavingStreams(models.Model):
#     stream_id = models.BigIntegerField(primary_key=True)
#     user_id_external = models.CharField(max_length=64)
#     source_login = models.ForeignKey(SourceLogins,
#                                      db_column='login_id',
#                                      on_delete=models.PROTECT)
#     saving_percentage = models.DecimalField(max_digits=5,
#                                             decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True,
#                                       null=True)
