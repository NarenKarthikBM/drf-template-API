from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView

from users.models import CustomUser
from users.serializers import UserSerializer
from users.utils import authorize_user
from users.validator import UserObtainAuthTokenInputValidator


class UserObtainAuthTokenAPI(APIView):
    """API view to obtain auth tokens

    Methods:
        POST
    """

    permission_classes = []
    authentication_classes = []

    def post(self, request):
        """POST Method to generate and serve the auth tokens

        Input Serializer:
            - email
            - password

        Output Serializer:
            - tokens
            - User Serializer (details_serializer)

        Possible Outputs:
            - Errors
                - User not found (email field)
                - incorrect password (password field)
            - Successes
                - tokens and user details

        """

        validated_data = UserObtainAuthTokenInputValidator(
            request.data
        ).serialized_data()
        user_authorization = authorize_user(validated_data)

        if not user_authorization:
            raise ValidationError({"error": "user not found", "field": "email"})

        if "error" in user_authorization:
            raise ValidationError({"error": "incorrect password", "field": "password"})

        return Response(user_authorization, status=status.HTTP_200_OK)
