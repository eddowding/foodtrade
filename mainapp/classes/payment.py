import stripe



STRIPE_API = 'sk_test_dj0ArFwwcCljH8n1aioJ6jtV'


stripe.api_key = STRIPE_API

print stripe.Charge.retrieve("ch_103SnR2nAKU9zlpXCk30naP1", expand=['customer'])