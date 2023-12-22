import psycopg2


try:
    connection = psycopg2.connect(
        host="127.0.0.1",
        user="postgres",
        password="12344321",
        database="MEME"
        )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
        "SELECT version();"
        )

        print(f"Сервер выдаёт {cursor.fetchone()}")



    with connection.cursor() as cursor:
        cursor.execute(
        """UPDATE user_meme
        SET save_pic = ARRAY_APPEND(save_pic, 2)
        WHERE user_ = '@Graff_Troll';"""
        )

except Exception as _ex:
    print("Ошибся бро", _ex)
finally:
    if connection:
        connection.close()
        print("Абоба")






    
