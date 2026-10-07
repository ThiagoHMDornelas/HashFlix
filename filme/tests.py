from django.test import TestCase
from django.urls import reverse

from .forms import CriarContaForm, FormHomepage
from .models import Episodio, Filme, Usuario
from .novos_context import lista_filmes_emalta, lista_filmes_recentes


def criar_filme(titulo='Filme Teste', categoria='OUTROS', visualizacoes=0):
    return Filme.objects.create(
        titulo=titulo,
        thumb='thumb_filmes/teste.png',
        descricao='Descrição de teste',
        categoria=categoria,
        visualizacoes=visualizacoes,
    )


class FilmeModelTest(TestCase):
    def test_str_retorna_titulo(self):
        filme = criar_filme(titulo='Python Impressionador')
        self.assertEqual(str(filme), 'Python Impressionador')

    def test_visualizacoes_inicia_em_zero(self):
        self.assertEqual(criar_filme().visualizacoes, 0)


class EpisodioModelTest(TestCase):
    def test_str_inclui_filme_e_titulo(self):
        filme = criar_filme(titulo='Power BI')
        episodio = Episodio.objects.create(
            filme=filme, titulo='Aula 1', video='https://youtu.be/x'
        )
        self.assertEqual(str(episodio), 'Power BI - Aula 1')


class UsuarioModelTest(TestCase):
    def test_criacao_de_usuario(self):
        usuario = Usuario.objects.create_user(
            username='joao', password='SenhaForte123'
        )
        self.assertEqual(usuario.username, 'joao')
        self.assertEqual(usuario.filmes_vistos.count(), 0)


class FormsTest(TestCase):
    def test_form_homepage_valido(self):
        self.assertTrue(FormHomepage(data={'email': 'teste@teste.com'}).is_valid())

    def test_form_homepage_invalido(self):
        self.assertFalse(FormHomepage(data={'email': 'nao-e-email'}).is_valid())

    def test_criar_conta_form_valido(self):
        form = CriarContaForm(data={
            'username': 'novo',
            'email': 'novo@teste.com',
            'password1': 'SenhaForte123',
            'password2': 'SenhaForte123',
        })
        self.assertTrue(form.is_valid())


class ContextProcessorsTest(TestCase):
    def test_listas_de_filmes(self):
        for i in range(3):
            criar_filme(titulo=f'Filme {i}', visualizacoes=i)

        recentes = lista_filmes_recentes(None)
        self.assertEqual(len(recentes['lista_filmes_recentes']), 3)
        self.assertIsNotNone(recentes['lista_destaque'])

        emalta = lista_filmes_emalta(None)
        self.assertEqual(len(emalta['lista_filmes_emalta']), 3)

    def test_destaque_nulo_sem_filmes(self):
        self.assertIsNone(lista_filmes_recentes(None)['lista_destaque'])


class HomepageViewTest(TestCase):
    def test_get_anonimo_renderiza_homepage(self):
        response = self.client.get(reverse('filme:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_autenticado_redireciona_para_homefilmes(self):
        Usuario.objects.create_user(username='joao', password='SenhaForte123')
        self.client.login(username='joao', password='SenhaForte123')
        response = self.client.get(reverse('filme:homepage'))
        self.assertRedirects(response, reverse('filme:homefilmes'))

    def test_email_existente_redireciona_para_login(self):
        Usuario.objects.create_user(
            username='joao', email='joao@teste.com', password='SenhaForte123'
        )
        response = self.client.post(
            reverse('filme:homepage'), {'email': 'joao@teste.com'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('from_homepage=true', response.url)

    def test_email_novo_redireciona_para_criar_conta(self):
        response = self.client.post(
            reverse('filme:homepage'), {'email': 'novo@teste.com'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('criarconta', response.url)


class HomeFilmesViewTest(TestCase):
    def test_requer_login(self):
        response = self.client.get(reverse('filme:homefilmes'))
        self.assertEqual(response.status_code, 302)

    def test_lista_filmes_para_autenticado(self):
        filme = criar_filme(titulo='Filme A')
        Usuario.objects.create_user(username='joao', password='SenhaForte123')
        self.client.login(username='joao', password='SenhaForte123')
        response = self.client.get(reverse('filme:homefilmes'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(filme, response.context['object_list'])


class DetalhesFilmeViewTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='joao', password='SenhaForte123'
        )
        self.filme = criar_filme(titulo='Filme Detalhe', categoria='PROGRAMACAO')
        self.client.login(username='joao', password='SenhaForte123')

    def test_conta_visualizacao_e_registra_historico(self):
        self.client.get(
            reverse('filme:detalhesfilme', kwargs={'pk': self.filme.pk})
        )
        self.filme.refresh_from_db()
        self.assertEqual(self.filme.visualizacoes, 1)
        self.assertTrue(
            self.usuario.filmes_vistos.filter(pk=self.filme.pk).exists()
        )


class PesquisarFilmeViewTest(TestCase):
    def setUp(self):
        Usuario.objects.create_user(username='joao', password='SenhaForte123')
        self.client.login(username='joao', password='SenhaForte123')

    def test_busca_por_titulo(self):
        filme_python = criar_filme(titulo='Python Impressionador')
        criar_filme(titulo='Excel Impressionador')
        response = self.client.get(
            reverse('filme:pesquisafilme'), {'query': 'Python'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertIn(filme_python, response.context['object_list'])


class CriarContaViewTest(TestCase):
    def test_cria_usuario_e_redireciona_para_login(self):
        response = self.client.post(reverse('filme:criarconta'), {
            'username': 'novo',
            'email': 'novo@teste.com',
            'password1': 'SenhaForte123',
            'password2': 'SenhaForte123',
        })
        self.assertRedirects(response, reverse('filme:login'))
        self.assertTrue(Usuario.objects.filter(username='novo').exists())


class PaginaPerfilViewTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='joao', password='SenhaForte123'
        )
        self.client.login(username='joao', password='SenhaForte123')

    def test_edita_proprio_perfil(self):
        response = self.client.get(
            reverse('filme:editarperfil', kwargs={'pk': self.usuario.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_redireciona_para_o_proprio_perfil(self):
        outro = Usuario.objects.create_user(
            username='maria', password='SenhaForte123'
        )
        response = self.client.get(
            reverse('filme:editarperfil', kwargs={'pk': outro.pk})
        )
        self.assertRedirects(
            response,
            reverse('filme:editarperfil', kwargs={'pk': self.usuario.pk}),
        )
