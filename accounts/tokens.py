from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class CustomPasswordResetToken(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return(
		six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.active)
		)

acount_confirm_token=CustomPasswordResetToken()