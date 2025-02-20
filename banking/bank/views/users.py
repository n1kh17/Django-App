from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserAPI(APIView):
    def get(self, request, user_id=None):
        """Retrieve a user or list all users."""
        try:
            with connection.cursor() as cursor:
                if user_id:
                    cursor.execute("SELECT get_user(%s)", [user_id])
                else:
                    cursor.execute("SELECT json_agg(get_user(user_id)) FROM users")
                
                result = cursor.fetchone()[0]  # Fetch the JSON result
                return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Create a new user."""
        username = request.data.get('username')
        email = request.data.get('email')
        password_hash = request.data.get('password_hash')

        if not all([username, email, password_hash]):
            return Response({"error": "All fields (username, email, password_hash) are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT create_user(%s, %s, %s)", [username, email, password_hash])
                result = cursor.fetchone()[0]
                return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, user_id):
        """Update an existing user."""
        username = request.data.get('username')
        email = request.data.get('email')

        if not all([username, email]):
            return Response({"error": "Both username and email are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT update_user(%s, %s, %s)", [user_id, username, email])
                result = cursor.fetchone()[0]
                return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, user_id):
        """Delete a user."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT delete_user(%s)", [user_id])
                result = cursor.fetchone()[0]
                return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
