import pymysql

def adiciona_usuario(conn, name, email, city):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO Users (fullName,email,city) VALUES (%s,%s,%s)', (name,email,city))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {name} na tabela users')

def acha_usuario(conn, nome):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idUser FROM Users WHERE fullName = %s', (nome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def muda_nome_usuario(conn, idUser, nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE Users SET fullName=%s where idUser=%s', (nome, idUser))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nome do id {idUser} para {nome} na tabela users')

def desativa_usuario(conn, idUser):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE Users SET activeUser=0 where idUser=%s', (idUser))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso desativar o {idUser} na tabela users')

def remove_usuario(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM Users WHERE idUser=%s', (id))

def lista_usuarios(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idUser, fullName from Users')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def lista_usuarios_ativos(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idUser, fullName from Users WHERE activeUser = 1')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def adiciona_post(conn, title,postText,urlPhoto,idUser):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO Posts (title,postText,urlPhoto,idUser) VALUES (%s,%s,%s,%s)', (title, postText,urlPhoto,idUser))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {title} na tabela Posts')

def acha_post(conn, titulo):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPost FROM Posts WHERE title = %s', (titulo))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def remove_post(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM Posts WHERE idPost=%s', (id))

def muda_titulo_post(conn, id, novo_titulo):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE Posts SET title=%s where idPost=%s', (novo_titulo, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar title do id {id} para {novo_titulo} na tabela posts')

def desativa_post(conn, id):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE Posts SET activePost=0 where idPost=%s', (id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso desativar o id {id} na tabela posts') 

def lista_post(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPost,title from Posts')
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def lista_post_ativos(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPost,title from Posts WHERE activePost = 1')
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def adiciona_passaro(conn,birdType):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO Birds (birdType) VALUES (%s)', (birdType))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {birdType} na tabela Birds')

def acha_passaro(conn, birdType):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idBird FROM Birds WHERE birdType = %s', (birdType))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def remove_passaro(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM Birds WHERE idBird=%s', (id))

def muda_tipo_passaro(conn, id, novo_tipo):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE Birds SET birdType=%s where idBird=%s', (novo_tipo, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar birdType do id {id} para {novo_tipo} na tabela Birds')

def lista_passaros(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idBird, birdType from Birds')
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros

def adiciona_preferencia(conn, idUser, idBird):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO Preferences (idUser, idBird) VALUES (%s, %s)', (idUser, idBird))

def remove_preferencia(conn, idUser, idBird):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM Preferences WHERE idUser=%s AND idBird=%s',(idUser, idBird))

def lista_preferido_por(conn, idBird):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idUser FROM Preferences WHERE idBird=%s', (idBird))
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def lista_prefere(conn, idUser):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idBird FROM Preferences WHERE idUser=%s', (idUser))
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros

def adiciona_mencao(conn, idPost, idUser):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO Mentions (idPost,idUser) VALUES (%s, %s)', (idPost, idUser))

def remove_mencao(conn, idPost, idUser):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM Mentions WHERE idPost=%s AND idUser=%s',(idPost, idUser))

def lista_mencionado_por(conn, idUser):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPost FROM Mentions WHERE idUser=%s', (idUser))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def lista_menciona(conn, idPost):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idUser FROM Mentions WHERE idPost=%s', (idPost))
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def adiciona_tag(conn, idPost, idBird):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO Tags (idPost,idBird) VALUES (%s, %s)', (idPost, idBird))

def remove_tag(conn, idPost, idBird):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM Tags WHERE idPost=%s AND idBird=%s',(idPost, idBird))

def lista_tagged_por(conn, idBird):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPost FROM Tags WHERE idBird=%s', (idBird))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def lista_tagged(conn, idPost):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idBird FROM Tags WHERE idPost=%s', (idPost))
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros

def adiciona_vizualizacao(conn, device, viewDate, browser, idUser, idPost):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO Views VALUES (%s, %s, %s, %s, %s)', (device,viewDate,browser,idUser,idPost))

def remove_vizualizacao(conn, idUser, idPost):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM Views WHERE idUser=%s AND idPost=%s',(idUser, idPost))

def lista_vizualizado_por(conn, idPost):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idUser FROM Views WHERE idPost=%s', (idPost))
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def lista_vizualizou(conn, idUser):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPost FROM Views WHERE idUser=%s', (idUser))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def lista_postado_pelo(conn, idUser):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPost from Posts WHERE idUser = %s', (idUser))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def lista_preferencia_ativas(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idUser, idBird from Preferences WHERE activePreference = 1')
        res = cursor.fetchall()
        preferences = tuple(x[0] for x in res)
        return preferences

def lista_preferencia(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idUser, idBird from Preferences')
        res = cursor.fetchall()
        preferences = tuple(x[0] for x in res)
        return preferences

def lista_mencao_ativas(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPost, idUser from Mentions WHERE activeMention = 1')
        res = cursor.fetchall()
        mentions = tuple(x[0] for x in res)
        return mentions

def lista_mencao(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPost, idUser from Mentions')
        res = cursor.fetchall()
        mentions = tuple(x[0] for x in res)
        return mentions

def lista_tag_ativas(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPost, idBird from Tags WHERE activeTag = 1')
        res = cursor.fetchall()
        tags = tuple(x[0] for x in res)
        return tags

def lista_tag(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPost, idBird from Tags')
        res = cursor.fetchall()
        tags = tuple(x[0] for x in res)
        return tags