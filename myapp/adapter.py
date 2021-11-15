from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super(AccountAdapter,self).save_user(request, user, form, commit=False)
        user.account_image = form.cleaned_data.get('account_image')
        user.save()