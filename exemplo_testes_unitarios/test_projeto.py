import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql

from projeto import *

class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='socialNetwork'
        )

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION')

    def tearDown(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('ROLLBACK')

    #################################################################################################################

    def test_adiciona_usuario(self):
        conn = self.__class__.connection
    
        nome = 'Rafael'
        email = 'rafael@email.com'
        cidade = 'São Paulo'

        # Adiciona um usuario não existente.
        adiciona_usuario(conn, nome, email, cidade)

        # Tenta adicionar o mesmo usuario duas vezes.
        try:
            adiciona_usuario(conn, nome, email, cidade)
            self.fail('Nao deveria ter adicionado o mesmo usuario duas vezes.')
        except ValueError as e:
            pass

        # Checa se o usuario existe.
        id = acha_usuario(conn, nome)
        self.assertIsNotNone(id)

        # Tenta achar um usuario inexistente.
        id = acha_usuario(conn, 'Felipe')
        self.assertIsNone(id)

    def test_remove_usuario(self):
        conn = self.__class__.connection
        adiciona_usuario(conn, 'Pedro', 'pedro@email.com', 'Peruibe')
        id = acha_usuario(conn, 'Pedro')

        res = lista_usuarios(conn)
        self.assertCountEqual(res, (id,))

        remove_usuario(conn, id)

        res = lista_usuarios(conn)
        self.assertFalse(res)

    def test_muda_nome_usuario(self):
        conn = self.__class__.connection

        adiciona_usuario(conn, 'Rafael', 'rafael@email.com', 'Peruibe')

        adiciona_usuario(conn, 'Igor', 'igor@email.com', 'Peruibe')
        id = acha_usuario(conn, 'Igor')

        # Tenta mudar nome para algum nome já existente.
        try:
            muda_nome_usuario(conn, id, 'Rafael')
            self.fail('Não deveria ter mudado o nome.')
        except ValueError as e:
            pass

        # Tenta mudar nome para nome inexistente.
        muda_nome_usuario(conn, id, 'Bruno')

        # Verifica se mudou.
        id_novo = acha_usuario(conn, 'Bruno')
        self.assertEqual(id, id_novo)

    def test_lista_usuarios(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem usuarios no sistema.
        res = lista_usuarios(conn)
        self.assertFalse(res)

        # Adiciona alguns usuarios.
        usuarios_id = []
        for p in ('Eduardo', 'Ricardo', 'Isadora'):
            adiciona_usuario(conn, p, p+'@email.com', 'Peruibe')
            usuarios_id.append(acha_usuario(conn, p))

        # Verifica se os usuarios foram adicionados corretamente.
        res = lista_usuarios(conn)
        self.assertCountEqual(res, usuarios_id)

        # Remove os usuarios.
        for p in usuarios_id:
            remove_usuario(conn, p)

        # Verifica que todos os usuarios foram removidos.
        res = lista_usuarios(conn)
        self.assertFalse(res)

#################################################################################################################

    def test_adiciona_post(self):
        conn = self.__class__.connection
    
        adiciona_usuario(conn, 'Jorge', 'jorge@email.com', 'Peruibe')
        id_user = acha_usuario(conn, 'Jorge')

        title = 'Ele comeu papel e olha no que deu!'
        text = 'Ele foi comer papel mas a mae dele nao deixou. Que cena!'
        photo = 'https://www.imgur.com/lalalalQueFoto_legal.html'

        # Adiciona um post não existente.
        adiciona_post(conn, title, text, photo, id_user)

        # Tenta adicionar o mesmo post duas vezes.
        try:
            adiciona_post(conn, title, text, photo, id_user)
            self.fail('Nao deveria ter adicionado o mesmo post duas vezes.')
        except ValueError as e:
            pass

        # Checa se o usuario existe.
        id = acha_post(conn, title)
        self.assertIsNotNone(id)

        # Tenta achar um usuario inexistente.
        id = acha_usuario(conn, 'Felipe')
        self.assertIsNone(id)

    def test_remove_post(self):
        conn = self.__class__.connection
        adiciona_usuario(conn, 'Jorge', 'jorge@email.com', 'Peruibe')
        id_user = acha_usuario(conn, 'Jorge')

        title = 'Ele comeu papel e olha no que deu!'
        text = 'Ele foi comer papel mas a mae dele nao deixou. Que cena!'
        photo = 'https://www.imgur.com/lalalalQueFoto_legal.html'
        adiciona_post(conn, title, text, photo, id_user)
        id = acha_post(conn, title)

        res = lista_post(conn)
        self.assertCountEqual(res, (id,))

        remove_post(conn, id)

        res = lista_post(conn)
        self.assertFalse(res)

    def test_muda_titulo_post(self):
        conn = self.__class__.connection

        adiciona_usuario(conn, 'Neusa', 'neusa@email.com', 'Peruibe')
        id_user = acha_usuario(conn, 'Neusa')

        title = 'Ele comeu pedra e olha no que deu!'
        text = 'Ele foi comer pedra mas o pai dele nao deixou. Que cena!'
        photo = 'https://www.imgur.com/a_foto_dele.html'
        adiciona_post(conn, title, text, photo, id_user)
        id = acha_post(conn, title)

        adiciona_post(conn, 'Ele comeu papel e olha no que deu!', text, photo, id_user)

        # Tenta mudar nome para algum titulo já existente.
        try:
            muda_titulo_post(conn, id, 'Ele comeu papel e olha no que deu!')
            self.fail('Não deveria ter mudado o titulo.')
        except ValueError as e:
            pass

        # Tenta mudar titulo para titulo inexistente.
        muda_titulo_post(conn, id, 'Ele comeu tesoura e olha no que deu!')

        # Verifica se mudou.
        id_novo = acha_post(conn, 'Ele comeu tesoura e olha no que deu!')
        self.assertEqual(id, id_novo)

    def test_lista_post(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem posts no sistema.
        res = lista_post(conn)
        self.assertFalse(res)

        adiciona_usuario(conn, 'Neura', 'neura@email.com', 'Peruibe')
        id_user = acha_usuario(conn, 'Neura')

        # Adiciona alguns posts.
        posts_id = []
        for p in ('Menino cai e se quebra.', 'Olha o que eu ganhei!', 'Ninguem segura essa figura!'):
            adiciona_post(conn, p, 'lala lalala lala al l alalalla ala al alala la', 'https://www.imgur.com/lalala', id_user)
            posts_id.append(acha_post(conn, p))

        # Verifica se os posts foram adicionados corretamente.
        res = lista_post(conn)
        self.assertCountEqual(res, posts_id)

        # Remove os usuarios.
        for p in posts_id:
            remove_post(conn, p)

        # Verifica que todos os usuarios foram removidos.
        res = lista_post(conn)
        self.assertFalse(res)

    #################################################################################################################

    def test_adiciona_passaro(self):
        conn = self.__class__.connection

        passaro = 'andorinha'

        # Adiciona passaro não existente.
        adiciona_passaro(conn, passaro)

        # Tenta adicionar a mesma passaro duas vezes.
        try:
            adiciona_passaro(conn, passaro)
            self.fail('Nao deveria ter adicionado a mesma passaro duas vezes.')
        except ValueError as e:
            pass

        # Checa se a passaro existe.
        id = acha_passaro(conn, passaro)
        self.assertIsNotNone(id)

        # Tenta achar uma passaro inexistente.
        id = acha_passaro(conn, 'gaviao')
        self.assertIsNone(id)

    def test_remove_passaro(self):
        conn = self.__class__.connection
        adiciona_passaro(conn, 'andorinha')
        id = acha_passaro(conn, 'andorinha')

        res = lista_passaros(conn)
        self.assertCountEqual(res, (id,))

        remove_passaro(conn, id)

        res = lista_passaros(conn)
        self.assertFalse(res)

    def test_muda_nome_passaro(self):
        conn = self.__class__.connection

        adiciona_passaro(conn, 'gaivota')
        adiciona_passaro(conn, 'canario')
        id = acha_passaro(conn, 'canario')

        # Tenta mudar nome para algum nome já existente.
        try:
            muda_tipo_passaro(conn, id, 'gaivota')
            self.fail('Não deveria ter mudado o nome.')
        except ValueError as e:
            pass

        # Tenta mudar nome para nome inexistente.
        muda_tipo_passaro(conn, id, 'macuco')

    def test_lista_passaros(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem passaros no sistema.
        res = lista_passaros(conn)
        self.assertFalse(res)

        # Adiciona algumas passaros.
        passaros_id = []
        for p in ('sabia', 'canario', 'pavao'):
            adiciona_passaro(conn, p)
            passaros_id.append(acha_passaro(conn, p))

        # Verifica se as passaros foram adicionadas corretamente.
        res = lista_passaros(conn)
        self.assertCountEqual(res, passaros_id)

        # Remove as passaros.
        for c in passaros_id:
            remove_passaro(conn, c)

        # Verifica que todos as passaros foram removidas.
        res = lista_passaros(conn)
        self.assertFalse(res)

    #################################################################################################################

    #@unittest.skip('Em desenvolvimento.')
    def test_adiciona_preferencia(self):
        conn = self.__class__.connection

        # Cria alguns passaros.
        adiciona_passaro(conn, 'andorinha')
        id_andorinha = acha_passaro(conn, 'andorinha')

        adiciona_passaro(conn, 'jacutinga')
        id_jacutinga = acha_passaro(conn, 'jacutinga')

        # Cria alguns usuarios.
        adiciona_usuario(conn, 'Guilherme', 'guilherme@email.com', 'Peruibe')
        id_Guilherme = acha_usuario(conn, 'Guilherme')
        
        adiciona_usuario(conn, 'Ricardo', 'Ricardo@email.com', 'Peruibe')
        id_Ricardo = acha_usuario(conn, 'Ricardo')
        
        adiciona_usuario(conn, 'Isadora', 'Isadora@email.com', 'Peruibe')
        id_Isadora = acha_usuario(conn, 'Isadora')

        adiciona_usuario(conn, 'Andrea', 'andrea@email.com', 'Peruibe')
        id_Andrea = acha_usuario(conn, 'Andrea')

        # Conecta passaros e usuarios.
        adiciona_preferencia(conn, id_Guilherme, id_andorinha)
        adiciona_preferencia(conn, id_Guilherme, id_jacutinga)
        adiciona_preferencia(conn, id_Andrea, id_andorinha)
        adiciona_preferencia(conn, id_Andrea, id_jacutinga)
        adiciona_preferencia(conn, id_Ricardo, id_andorinha)
        adiciona_preferencia(conn, id_Isadora, id_jacutinga)

        res = lista_prefere(conn, id_Guilherme)
        self.assertCountEqual(res, (id_andorinha, id_jacutinga))

        res = lista_prefere(conn, id_Andrea)
        self.assertCountEqual(res, (id_andorinha, id_jacutinga))

        res = lista_prefere(conn, id_Ricardo)
        self.assertCountEqual(res, (id_andorinha,))

        res = lista_prefere(conn, id_Isadora)
        self.assertCountEqual(res, (id_jacutinga,))

        res = lista_preferido_por(conn, id_andorinha)
        self.assertCountEqual(res, (id_Guilherme, id_Andrea, id_Ricardo))

        res = lista_preferido_por(conn, id_jacutinga)
        self.assertCountEqual(res, (id_Guilherme, id_Andrea, id_Isadora))

        # Testa se a remoção de uma passaro causa a remoção das relações entre essa passaro e seus usuarios.
        remove_passaro(conn, id_jacutinga)

        res = lista_prefere(conn, id_Guilherme)
        self.assertCountEqual(res, (id_andorinha,))

        res = lista_prefere(conn, id_Andrea)
        self.assertCountEqual(res, (id_andorinha,))

        res = lista_prefere(conn, id_Isadora)
        self.assertFalse(res)

        # Testa se a remoção de um usuario causa a remoção das relações entre esse usuario e suas passaros.
        remove_usuario(conn, id_Andrea)

        res = lista_preferido_por(conn, id_andorinha)
        self.assertCountEqual(res, (id_Guilherme, id_Ricardo))

        # Testa a remoção específica de uma relação usuario-passaro.
        remove_preferencia(conn, id_Guilherme, id_andorinha)

        res = lista_preferido_por(conn, id_andorinha)
        self.assertCountEqual(res, (id_Ricardo,))

    #################################################################################################################

    #@unittest.skip('Em desenvolvimento.')
    def test_adiciona_mencao(self):
        conn = self.__class__.connection

        # Cria alguns usuarios.
        adiciona_usuario(conn, 'Guilherme', 'guilherme@email.com', 'Peruibe')
        id_Guilherme = acha_usuario(conn, 'Guilherme')
        
        adiciona_usuario(conn, 'Ricardo', 'Ricardo@email.com', 'Peruibe')
        id_Ricardo = acha_usuario(conn, 'Ricardo')
        
        adiciona_usuario(conn, 'Isadora', 'Isadora@email.com', 'Peruibe')
        id_Isadora = acha_usuario(conn, 'Isadora')

        adiciona_usuario(conn, 'Andrea', 'andrea@email.com', 'Peruibe')
        id_Andrea = acha_usuario(conn, 'Andrea')

        adiciona_usuario(conn, 'Neura', 'neura@email.com', 'Peruibe')
        id_neura = acha_usuario(conn, 'Neura')

        # Cria alguns posts.
        posts_id = []
        for p in ('Menino cai e se quebra.', 'Olha o que eu ganhei!', 'Ninguem segura essa figura!'):
            adiciona_post(conn, p, 'lala lalala lala al l alalalla ala al alala la', 'https://www.imgur.com/lalala', id_neura)
            posts_id.append(acha_post(conn, p))

        # Conecta posts e usuarios.
        adiciona_mencao(conn, posts_id[0], id_Guilherme)
        adiciona_mencao(conn, posts_id[1], id_Guilherme)
        adiciona_mencao(conn, posts_id[0], id_Andrea)
        adiciona_mencao(conn, posts_id[1], id_Andrea)
        adiciona_mencao(conn, posts_id[0], id_Ricardo)
        adiciona_mencao(conn, posts_id[1], id_Isadora)

        res = lista_mencionado_por(conn, id_Guilherme)
        self.assertCountEqual(res, (posts_id[0], posts_id[1]))

        res = lista_mencionado_por(conn, id_Andrea)
        self.assertCountEqual(res, (posts_id[0], posts_id[1]))

        res = lista_mencionado_por(conn, id_Ricardo)
        self.assertCountEqual(res, (posts_id[0],))

        res = lista_mencionado_por(conn, id_Isadora)
        self.assertCountEqual(res, (posts_id[1],))

        res = lista_menciona(conn, posts_id[0])
        self.assertCountEqual(res, (id_Guilherme, id_Andrea, id_Ricardo))

        res = lista_menciona(conn, posts_id[1])
        self.assertCountEqual(res, (id_Guilherme, id_Andrea, id_Isadora))

        # Testa se a remoção de um post causa a remoção das relações entre esse post e seus usuarios.
        remove_post(conn, posts_id[1])

        res = lista_mencionado_por(conn, id_Guilherme)
        self.assertCountEqual(res, (posts_id[0],))

        res = lista_mencionado_por(conn, id_Andrea)
        self.assertCountEqual(res, (posts_id[0],))

        res = lista_mencionado_por(conn, id_Isadora)
        self.assertFalse(res)

        # Testa se a remoção de um usuario causa a remoção das relações entre esse usuario e seus posts.
        remove_usuario(conn, id_Andrea)

        res = lista_menciona(conn, posts_id[0])
        self.assertCountEqual(res, (id_Guilherme, id_Ricardo))

        # Testa a remoção específica de uma relação usuario-post.
        remove_mencao(conn, id_Guilherme, posts_id[0])

        res = lista_menciona(conn, posts_id[0])
        self.assertCountEqual(res, (id_Ricardo,))

    #################################################################################################################

    #@unittest.skip('Em desenvolvimento.')
    def test_adiciona_tag(self):
        conn = self.__class__.connection

        # Cria alguns passaros.
        passaros_id = []
        for i in ('periquito', 'gaivota', 'pomba', 'sabia'):
            adiciona_passaro(conn, i)
            passaros_id.append(acha_passaro(conn, i))


        adiciona_usuario(conn, 'Neura', 'neura@email.com', 'Peruibe')
        id_neura = acha_usuario(conn, 'Neura')

        # Cria alguns posts.
        posts_id = []
        for p in ('Menino cai e se quebra.', 'Olha o que eu ganhei!', 'Ninguem segura essa figura!'):
            adiciona_post(conn, p, 'lala lalala lala al l alalalla ala al alala la', 'https://www.imgur.com/lalala', id_neura)
            posts_id.append(acha_post(conn, p))

        # Conecta posts e passaros.
        adiciona_tag(conn, posts_id[0], passaros_id[0])
        adiciona_tag(conn, posts_id[1], passaros_id[0])
        adiciona_tag(conn, posts_id[0], passaros_id[1])
        adiciona_tag(conn, posts_id[1], passaros_id[1])
        adiciona_tag(conn, posts_id[0], passaros_id[2])
        adiciona_tag(conn, posts_id[1], passaros_id[3])

        res = lista_tagged_por(conn, passaros_id[0])
        self.assertCountEqual(res, (posts_id[0], posts_id[1]))

        res = lista_tagged_por(conn, passaros_id[1])
        self.assertCountEqual(res, (posts_id[0], posts_id[1]))

        res = lista_tagged_por(conn, passaros_id[2])
        self.assertCountEqual(res, (posts_id[0],))

        res = lista_tagged_por(conn, passaros_id[3])
        self.assertCountEqual(res, (posts_id[1],))

        res = lista_tagged(conn, posts_id[0])
        self.assertCountEqual(res, (passaros_id[0], passaros_id[1], passaros_id[2]))

        res = lista_tagged(conn, posts_id[1])
        self.assertCountEqual(res, (passaros_id[0], passaros_id[1], passaros_id[3]))

        # Testa se a remoção de um post causa a remoção das relações entre esse post e seus passaros.
        remove_post(conn, posts_id[1])

        res = lista_tagged_por(conn, passaros_id[0])
        self.assertCountEqual(res, (posts_id[0],))

        res = lista_tagged_por(conn, passaros_id[1])
        self.assertCountEqual(res, (posts_id[0],))

        res = lista_tagged_por(conn, passaros_id[3])
        self.assertFalse(res)

        # Testa se a remoção de um passaro causa a remoção das relações entre esse passaro e seus posts.
        remove_passaro(conn, passaros_id[1])

        res = lista_tagged(conn, posts_id[0])
        self.assertCountEqual(res, (passaros_id[0], passaros_id[2]))

        # Testa a remoção específica de uma relação passaro-post.
        remove_tag(conn, posts_id[0], passaros_id[0])

        res = lista_tagged(conn, posts_id[0])
        self.assertCountEqual(res, (passaros_id[2],))

    #################################################################################################################

    #@unittest.skip('Em desenvolvimento.')
    def test_adiciona_view(self):
        conn = self.__class__.connection

        # Cria alguns usuarios.
        adiciona_usuario(conn, 'Guilherme', 'guilherme@email.com', 'Peruibe')
        id_Guilherme = acha_usuario(conn, 'Guilherme')
        
        adiciona_usuario(conn, 'Ricardo', 'Ricardo@email.com', 'Peruibe')
        id_Ricardo = acha_usuario(conn, 'Ricardo')
        
        adiciona_usuario(conn, 'Isadora', 'Isadora@email.com', 'Peruibe')
        id_Isadora = acha_usuario(conn, 'Isadora')

        adiciona_usuario(conn, 'Andrea', 'andrea@email.com', 'Peruibe')
        id_Andrea = acha_usuario(conn, 'Andrea')

        adiciona_usuario(conn, 'Neura', 'neura@email.com', 'Peruibe')
        id_neura = acha_usuario(conn, 'Neura')

        # Cria alguns posts.
        posts_id = []
        for p in ('Menino cai e se quebra.', 'Olha o que eu ganhei!', 'Ninguem segura essa figura!'):
            adiciona_post(conn, p, 'lala lalala lala al l alalalla ala al alala la', 'https://www.imgur.com/lalala', id_neura)
            posts_id.append(acha_post(conn, p))

        # Conecta posts e usuarios.
        adiciona_vizualizacao(conn, 'IPhone 5', '2004-05-23T14:25:10', 'Chrome', id_Guilherme, posts_id[0])
        adiciona_vizualizacao(conn, 'IPhone 5', '2004-05-23T14:25:10', 'Chrome', id_Guilherme, posts_id[1])
        adiciona_vizualizacao(conn, 'IPhone 5', '2004-05-23T14:25:10', 'Chrome', id_Andrea, posts_id[0])
        adiciona_vizualizacao(conn, 'IPhone 5', '2004-05-23T14:25:10', 'Chrome', id_Andrea, posts_id[1])
        adiciona_vizualizacao(conn, 'IPhone 5', '2004-05-23T14:25:10', 'Chrome', id_Ricardo, posts_id[0])
        adiciona_vizualizacao(conn, 'IPhone 5', '2004-05-23T14:25:10', 'Chrome', id_Isadora, posts_id[1])

        res = lista_vizualizou(conn, id_Guilherme)
        self.assertCountEqual(res, (posts_id[0], posts_id[1]))

        res = lista_vizualizou(conn, id_Andrea)
        self.assertCountEqual(res, (posts_id[0], posts_id[1]))

        res = lista_vizualizou(conn, id_Ricardo)
        self.assertCountEqual(res, (posts_id[0],))

        res = lista_vizualizou(conn, id_Isadora)
        self.assertCountEqual(res, (posts_id[1],))

        res = lista_vizualizado_por(conn, posts_id[0])
        self.assertCountEqual(res, (id_Guilherme, id_Andrea, id_Ricardo))

        res = lista_vizualizado_por(conn, posts_id[1])
        self.assertCountEqual(res, (id_Guilherme, id_Andrea, id_Isadora))

        # Testa se a remoção de um post causa a remoção das relações entre esse post e seus usuarios.
        remove_post(conn, posts_id[1])

        res = lista_vizualizou(conn, id_Guilherme)
        self.assertCountEqual(res, (posts_id[0],))

        res = lista_vizualizou(conn, id_Andrea)
        self.assertCountEqual(res, (posts_id[0],))

        res = lista_vizualizou(conn, id_Isadora)
        self.assertFalse(res)

        # Testa se a remoção de um usuario causa a remoção das relações entre esse usuario e seus posts.
        remove_usuario(conn, id_Andrea)

        res = lista_vizualizado_por(conn, posts_id[0])
        self.assertCountEqual(res, (id_Guilherme, id_Ricardo))

        # Testa a remoção específica de uma relação usuario-post.
        remove_vizualizacao(conn, id_Guilherme, posts_id[0])

        res = lista_vizualizado_por(conn, posts_id[0])
        self.assertCountEqual(res, (id_Ricardo,))

    #################################################################################################################

    #@unittest.skip('Em desenvolvimento.')
    def test_desativa(self):
        conn = self.__class__.connection

        # Cria alguns usuarios.
        adiciona_usuario(conn, 'Guilherme', 'guilherme@email.com', 'Peruibe')
        id_Guilherme = acha_usuario(conn, 'Guilherme')
        
        adiciona_usuario(conn, 'Ricardo', 'Ricardo@email.com', 'Peruibe')
        id_Ricardo = acha_usuario(conn, 'Ricardo')
        
        adiciona_usuario(conn, 'Isadora', 'Isadora@email.com', 'Peruibe')
        id_Isadora = acha_usuario(conn, 'Isadora')

        adiciona_usuario(conn, 'Andrea', 'andrea@email.com', 'Peruibe')
        id_Andrea = acha_usuario(conn, 'Andrea')

        adiciona_usuario(conn, 'Neura', 'neura@email.com', 'Peruibe')
        id_neura = acha_usuario(conn, 'Neura')

        # Cria alguns posts.
        posts_id = []
        for p in ('Menino cai e se quebra.', 'Olha o que eu ganhei!', 'Ninguem segura essa figura!'):
            adiciona_post(conn, p, 'lala lalala lala al l alalalla ala al alala la', 'https://www.imgur.com/lalala', id_neura)
            posts_id.append(acha_post(conn, p))

        adiciona_post(conn, 'Post Novo', 'lala lalala lala al l alalalla ala al alala la', 'https://www.imgur.com/lalala', id_Ricardo)

        # Cria alguns passaros.
        passaros_id = []
        for i in ('periquito', 'gaivota', 'pomba', 'sabia'):
            adiciona_passaro(conn, i)
            passaros_id.append(acha_passaro(conn, i))

        # Conecta posts e usuarios.
        adiciona_mencao(conn, posts_id[0], id_Guilherme)
        adiciona_mencao(conn, posts_id[1], id_Guilherme)
        adiciona_mencao(conn, posts_id[0], id_Andrea)
        adiciona_mencao(conn, posts_id[1], id_Andrea)
        adiciona_mencao(conn, posts_id[0], id_Ricardo)
        adiciona_mencao(conn, posts_id[1], id_Isadora)

        # Conecta posts e passaros.
        adiciona_tag(conn, posts_id[0], passaros_id[0])
        adiciona_tag(conn, posts_id[1], passaros_id[0])
        adiciona_tag(conn, posts_id[0], passaros_id[1])
        adiciona_tag(conn, posts_id[1], passaros_id[1])
        adiciona_tag(conn, posts_id[0], passaros_id[2])
        adiciona_tag(conn, posts_id[1], passaros_id[3])

        # Conecta passaros e usuarios.
        adiciona_preferencia(conn, id_Guilherme, passaros_id[0])
        adiciona_preferencia(conn, id_Guilherme, passaros_id[1])
        adiciona_preferencia(conn, id_Andrea, passaros_id[0])
        adiciona_preferencia(conn, id_Andrea, passaros_id[1])
        adiciona_preferencia(conn, id_Ricardo, passaros_id[0])
        adiciona_preferencia(conn, id_Isadora, passaros_id[1])


        # Testa se a desativacao de um post
        desativa_post(conn, posts_id[0])
        res1 = lista_post_ativos(conn)
        self.assertLess(len(res1), len(lista_post(conn)))

        # Testa se a desativacao de uma mencao com a desativacao de um post
        res2 = lista_mencao_ativas(conn)
        self.assertLess(len(res2), len(lista_mencao(conn)))

        # Testa se a desativacao de uma tag com a desativacao de um post
        res = lista_tag_ativas(conn)
        self.assertLess(len(res), len(lista_tag(conn)))

        # Testa se a desativacao de um usuario causa a desativacao das relações entre esse usuario e seus posts.
        desativa_usuario(conn, id_Isadora)

        res = lista_preferencia_ativas(conn)
        self.assertLess(len(res), len(lista_preferencia(conn)))

        res = lista_mencao_ativas(conn)
        self.assertLess(len(res), len(res2))

        res = lista_usuarios_ativos(conn)
        self.assertLess(len(res), len(lista_usuarios(conn)))

        # Testa se a desativacao de um usuario causa a desativacao dos seus posts.
        desativa_usuario(conn, id_Ricardo)

        res = lista_post_ativos(conn)
        self.assertLess(len(res), len(res1))


def run_sql_script(filename):
    global config
    with open(filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'], 
                '-u', config['USER'], 
                '-p' + config['PASS'], 
                '-h', config['HOST']
            ], 
            stdin=f
        )

def setUpModule():
    filenames = [entry for entry in os.listdir() 
        if os.path.isfile(entry) and re.match(r'.*_\d{3}\.sql', entry)]
    for filename in filenames:
        run_sql_script(filename)

def tearDownModule():
    run_sql_script('tear_down.sql')

if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)
