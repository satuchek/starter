from config import URL, CALLBACK_URL, AUDIENCE, CLIENT_ID

def build_login_link(callbackURL=''):
    login_link = 'https://' \
        + URL \
        + '.auth0.com/authorize?audience=' \
        + AUDIENCE \
        + '&response_type=token&client_id=' \
        + CLIENT_ID \
        + '&redirect_uri=' \
        + CALLBACK_URL


