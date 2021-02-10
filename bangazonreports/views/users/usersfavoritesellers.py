import sqlite3
from django.shortcuts import render
from bangazonapi.models import Customer
from bangazonapi.models import Favorite
from bangazonreports.views import Connection

def userfavseller_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    f.id,
                    f.customer_id,
                    f.seller_id,
                    u.id user_id,
                    u.first_name || ' ' || u.last_name AS full_name
                FROM
                    bangazonapi_favorite f
                JOIN
                    bangazonapi_customer c ON f.customer_id = c.id
                JOIN
                    auth_user u ON c.user_id = u.id             
            """)

            dataset = db_cursor.fetchall()

            sellers_by_user = {}

            for row in dataset:
                favorite = Favorite()
                favorite.customer = row["customer_id"]
                favorite.seller = row["seller_id"]

                uid = row["user_id"]

                if uid in sellers_by_user:

                    sellers_by_user[uid]['favorites'].append(favorite)

                else:
                    sellers_by_user[uid] = {}
                    sellers_by_user[uid]["id"] = uid
                    sellers_by_user[uid]["full_name"] = row["full_name"]
                    sellers_by_user[uid]["favorites"] = [favorite]


        list_of_users_favorite_sellers = sellers_by_user.values()

        template = 'users/list_of_favorites.html'
        context = {
            'userfavseller_list': list_of_users_favorite_sellers
        }

        return render(request, template, context)
