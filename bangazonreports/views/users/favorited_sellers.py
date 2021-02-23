import sqlite3
from django.shortcuts import render
from bangazonapi.models import Product
from bangazonreports.views import Connection


def favorited_sellers(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
              SELECT
	              cust.first_name || ' ' || cust.last_name AS customer_name,
                fav.first_name || ' ' || fav.last_name AS favorite_name
              FROM 
                bangazonapi_favorite f
              JOIN  
                bangazonapi_customer c ON c.id = f.customer_id
              JOIN 
                auth_user cust ON c.user_id = cust.id
              JOIN 
                bangazonapi_customer c2 ON c2.id = f.seller_id
              JOIN 
                auth_user fav ON c2.user_id = fav.id
            """)

            dataset = db_cursor.fetchall()

            favorites = {}

            for row in dataset:
              customer = row['customer_name']
              if customer in favorites:
                favorites[customer].append(row['favorite_name'])
              else:
                favorites[customer] = []
                favorites[customer].append(row['favorite_name'])

                
        # Get only the values from the dictionary and create a list from them
        list_of_favorites = favorites

        # Specify the Django template and provide data context
        template = 'users/favorited_sellers.html'
        context = {
            'report_title': 'Favorited Sellers By User',
            'favorites_list': list_of_favorites
        }

        return render(request, template, context)
