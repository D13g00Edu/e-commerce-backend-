const createFakePaymentIntent = async ({ amount, currency = 'usd' }) => {
  const fakeId = `pi_fake_${Date.now()}`;
  const clientSecret = `${fakeId}_secret_fake`;

  return {
    id: fakeId,
    object: 'payment_intent',
    amount,
    currency,
    status: 'requires_payment_method',
    client_secret: clientSecret,
  };
};

const confirmFakePaymentIntent = async (paymentIntentId) => {
  return {
    id: paymentIntentId,
    object: 'payment_intent',
    status: 'succeeded',
  };
};

module.exports = {
  createFakePaymentIntent,
  confirmFakePaymentIntent,
};