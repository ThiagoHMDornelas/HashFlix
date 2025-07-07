from django.shortcuts import render
from .models import Filme
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# def homepage(request):
#     return render(request, "homepage.html")

class Homepage(TemplateView):
    template_name = "homepage.html"


# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all()
#     context['lista_filmes'] = lista_filmes
#     return render(request, "homefilmes.html", context)

class HomeFilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme # passa para o HTML com o nome (object_list -> lista de itens do modelo)

class DetalhesFilme(LoginRequiredMixin, DetailView):
    template_name = 'detalhesfilme.html'
    model = Filme # object_list -> 1 item do modelo

    def get(self, request, *args, **kwargs):
        # contabilizar uma visualizaçao
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs) # redireciona o user para a url final

    def get_context_data(self, **kwargs):
        context = super(DetalhesFilme, self).get_context_data(**kwargs)
        # filtrar a minha tabela de filmes pegando os filmes cuja categoria é igual a categoria do filme da pagina (object)
        filmes_relacionados = self.model.objects.filter(categoria=self.get_object().categoria)[0:5]
        context['filmes_relacionados'] = filmes_relacionados
        return context

class PesquisarFilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme # passa para o HTML com o nome (object_list -> lista de itens do modelo)

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None