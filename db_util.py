import pymysql
import pymysql.cursors
import settings


def db_access(sqlProc, sqlArgs):
    try:
        dbConnection = pymysql.connect(
            host=settings.DB_HOST,
			port=settings.PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_DATABASE,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        cursor = dbConnection.cursor()
        cursor.callproc(sqlProc, sqlArgs)
        rows = cursor.fetchall()
        dbConnection.commit()
        cursor.close()
    except pymysql.MySQLError as e:
        return 0
    finally:
        dbConnection.commit()
        dbConnection.close()
    return rows


def db_direct(sqlCode):
    try:
        dbConnection = pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_DATABASE,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        cursor = dbConnection.cursor()
        cursor.execute(sqlCode)
        rows = cursor.fetchall()
        dbConnection.commit()
        cursor.close()
    except pymysql.MySQLError as e:
        return 0
    finally:
        dbConnection.commit()
        dbConnection.close()

    return rows


def checkAdmin(user):
    try:
        dbConnection = pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_DATABASE,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        cursor = dbConnection.cursor()
        cursor.callproc("getAdminByUsername", [user])
        count = len(cursor.fetchall())
        dbConnection.commit()
        cursor.close()
    except pymysql.MySQLError as e:
        raise Exception('Database Error:'+str(e))
    finally:
        dbConnection.commit()
        dbConnection.close()

    return count


def checkUser(user):
    try:
        dbConnection = pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_DATABASE,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        cursor = dbConnection.cursor()
        cursor.callproc("getUserByUsername", [user])
        count = len(cursor.fetchall())
        dbConnection.commit()
        cursor.close()
    except pymysql.MySQLError as e:
        raise Exception('Database Error:'+str(e)+ " ARGS: " + user)
    finally:
        dbConnection.commit()
        dbConnection.close()

    return count
