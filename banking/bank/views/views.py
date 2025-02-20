from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection

# Frontend view to list users and display a form for creating a user
def users_view(request):
    if request.method == "POST":
        # Process form data for creating a new user
        username = request.POST.get('username')
        email = request.POST.get('email')
        password_hash = request.POST.get('password_hash')
        
        if not all([username, email, password_hash]):
            messages.error(request, "All fields are required.")
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT create_user(%s, %s, %s)", [username, email, password_hash])
                    result = cursor.fetchone()[0]
                messages.success(request, "User created successfully!")
            except Exception as e:
                messages.error(request, f"Error creating user: {str(e)}")
        
        return redirect('users')

    # ✅ Correct way to fetch all users
    with connection.cursor() as cursor:
        cursor.execute("SELECT get_all_users()")  # Call function directly
        data = cursor.fetchone()[0] or []  # Fetch JSON

    return render(request, 'bank/users.html', {'users': data})


def accounts_view(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        account_number = request.POST.get('account_number')
        account_type = request.POST.get('account_type')

        if not all([user_id, account_number, account_type]):
            messages.error(request, "All fields are required.")
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT create_account(%s, %s, %s)", [user_id, account_number, account_type])
                    result = cursor.fetchone()[0]
                messages.success(request, "Account created successfully!")
            except Exception as e:
                messages.error(request, f"Error creating account: {str(e)}")
        return redirect('accounts')
    
    # ✅ Correct way to fetch all accounts
    with connection.cursor() as cursor:
        cursor.execute("SELECT get_all_accounts()")  # Call function directly
        data = cursor.fetchone()[0] or []

    return render(request, 'bank/accounts.html', {'accounts': data})
# def accounts_view(request):
#     """Retrieve all accounts from PostgreSQL function."""
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT get_all_accounts()")  # ✅ Fetch accounts
#             accounts = cursor.fetchone()[0] or []  # Ensure valid JSON response

#         print("Accounts Data:", accounts)  # 🔍 Debugging

#         return render(request, "bank/accounts.html", {"accounts": accounts})

#     except Exception as e:
#         return render(request, "bank/accounts.html", {"error": str(e), "accounts": []})

