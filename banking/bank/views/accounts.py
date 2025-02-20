from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AccountAPI(APIView):
    def post(self, request):
        """Create an account."""
        user_id = request.data.get('user_id')
        account_number = request.data.get('account_number')
        account_type = request.data.get('account_type')

        if not all([user_id, account_number, account_type]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT create_account(%s, %s, %s)", [user_id, account_number, account_type])
                result = cursor.fetchone()[0]  # Fetch JSON from PostgreSQL

            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, account_id=None):
        """Retrieve an account by ID."""
        try:
            with connection.cursor() as cursor:
                if account_id:
                    cursor.execute("SELECT get_account(%s)", [account_id])
                else:
                    cursor.execute("SELECT json_agg(get_account(account_id)) FROM accounts")

                result = cursor.fetchone()[0]  # Fetch JSON response
                return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, account_id):
        """Update an account."""
        account_type = request.data.get('account_type')
        balance = request.data.get('balance')

        if not all([account_type, balance]):
            return Response({"error": "Both account_type and balance are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT update_account(%s, %s, %s)", [account_id, account_type, balance])
                result = cursor.fetchone()[0]

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, account_id):
        """Delete an account."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT delete_account(%s)", [account_id])
                result = cursor.fetchone()[0]

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
