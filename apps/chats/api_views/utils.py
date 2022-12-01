from rest_framework.authtoken.models import Token


def auth_response(user, serializer):
    '''Auth Response for each authentication

    return data with user token.
    NOTE : Just for authentication not for getting a given user
    '''
    token = Token.objects.get(user=user)
    return {
        **serializer.data, 'token': token.key
    }
