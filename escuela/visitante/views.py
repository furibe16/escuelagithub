import os

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.list import ListView

from core.forms import CursoForm
from core.models import curso
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from visitante.forms import AlcanceForm, RecomendacionForm, CapituloForm, TemaForm, DetalleForm
from visitante.models import alcance, recomendacion, capitulo, tema, detalle


def homeView(request):
    mensaje_adicional = {'mensaje': 'Este es un mensaje adicional'}
    return render(request, "home1.html", mensaje_adicional)


class CursoListBusquedaView(ListView):
    model = curso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        criterio = self.request.GET['criterio']
        lista = None
        if criterio == '*':
            lista = curso.objects.filter(completo=True)
        elif criterio != '':
            lista = (curso.objects.filter(titulo__icontains=criterio) | curso.objects.filter(
                descripcion__icontains=criterio)) & curso.objects.filter(completo=True)

        context['lista'] = lista

        return context


class CursoCreateView(CreateView):
    model = curso
    form_class = CursoForm
    template_name = "visitante/curso_form.html"

    # success_url = reverse_lazy('core:home')

    def get_success_url(self):
        return reverse_lazy('core:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_template'] = 'Registro de un nuevo Curso'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        usuario = request.user
        if form.is_valid():
            curso1 = form.save(commit=False)
            curso1.profesor = usuario
            curso1.save()
            if usuario.first_name == 'm':
                usuario.first_name = 'p'
            elif usuario.first_name == 'a':
                usuario.first_name = 'b'
            usuario.save()
            return HttpResponseRedirect(self.get_success_url())
        return render(request, 'core/curso_form.html', {'form': form})


class CursoUpdateView(UpdateView):
    model = curso
    form_class = CursoForm
    template_name_suffix = '_update_form'
    # template_name = "visitante/curso_form.html"
    success_url = reverse_lazy('core:en_preparacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso1 = self.object
        context['titulo_template'] = 'Edicion de: '
        context['titulo'] = curso1.titulo
        # Lista de alcances
        context['lista_alcances'] = alcance.objects.filter(curso=curso1)
        # Lista de recomendaciones
        context['lista_recomendacion'] = recomendacion.objects.filter(curso=curso1)
        # Lista de capitulos
        context['lista_capitulos'] = capitulo.objects.filter(curso=curso1)
        return context


class CursoDeleteView(DeleteView):
    model = curso
    success_url = reverse_lazy('core:en_preparacion')


class CursoDetailView(DetailView):
    model = curso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estado = 'n'
        if not self.request.user == AnonymousUser():
            estado = 's'
        context['estado'] = estado
        context['reviews'] = 60
        # Lista de alcances
        context['lista_alcances'] = alcance.objects.filter(curso=self.object)
        # Lista de recomendaciones
        context['lista_recomendaciones'] = recomendacion.objects.filter(curso=self.object)
        # Lista de capitulos
        context['lista_capitulos'] = capitulo.objects.filter(curso=self.object)
        return context


class AlcanceCreateView(CreateView):
    model = alcance
    form_class = AlcanceForm
    template_name = "visitante/alcance_form.html"

    # success_url = reverse_lazy('core:lista_disciplinas')

    def get_success_url(self, *args):
        return reverse_lazy('visitante:editar_curso', args=[args[0].id]) + '?correcto=ok'

    def get_context_data(self):
        context = super(AlcanceCreateView, self).get_context_data()
        curso1 = curso.objects.get(id=self.request.GET['curso_id'])
        context['curso'] = curso1
        context['titulo_template'] = 'Nuevo alcance'
        context['titulo'] = curso1.titulo
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        curso1 = curso.objects.get(id=request.POST['curso_id'])
        if form.is_valid():
            alcance1 = form.save(commit=False)
            alcance1.curso = curso1
            alcance1.save()
            return HttpResponseRedirect(self.get_success_url(curso1))
        return render(request, 'visitante/alcance_form.html', {'form': form, 'curso': curso1})


class AlcanceUpdateView(UpdateView):
    model = alcance
    form_class = AlcanceForm
    template_name_suffix = '_update_form'

    # template_name = "visitante/alcance_form.html"

    def get_success_url(self):
        return reverse_lazy('visitante:editar_curso', args=[self.request.POST['curso_id']]) + '?correcto=ok'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = curso.objects.get(id=self.request.GET['curso_id'])
        context['titulo_template'] = 'Edicion de alcance'
        context['titulo'] = context['curso'].titulo

        return context


class AlcanceDeleteView(DeleteView):
    model = alcance

    # success_url = reverse_lazy('visitante:en_preparacion')

    def get_success_url(self):
        return reverse_lazy('visitante:editar_curso', args=[self.request.GET['curso_id']]) + '?correcto=ok'


class RecomendacionCreateView(CreateView):
    model = recomendacion
    form_class = RecomendacionForm
    template_name = "visitante/recomendacion_form.html"

    # success_url = reverse_lazy('core:lista_disciplinas')

    def get_success_url(self, *args):
        return reverse_lazy('visitante:editar_curso', args=[args[0].id]) + '?correcto=ok'

    def get_context_data(self):
        context = super(RecomendacionCreateView, self).get_context_data()
        curso1 = curso.objects.get(id=self.request.GET['curso_id'])
        context['curso'] = curso1
        context['titulo_template'] = 'Nuevo alcance'
        context['titulo'] = curso1.titulo
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        curso1 = curso.objects.get(id=request.POST['curso_id'])
        if form.is_valid():
            alcance1 = form.save(commit=False)
            alcance1.curso = curso1
            alcance1.save()
            return HttpResponseRedirect(self.get_success_url(curso1))
        return render(request, 'visitante/recomendacion_form.html', {'form': form, 'curso': curso1})


class RecomendacionUpdateView(UpdateView):
    model = recomendacion
    form_class = RecomendacionForm
    template_name_suffix = '_update_form'

    # template_name = "visitante/alcance_form.html"

    def get_success_url(self):
        return reverse_lazy('visitante:editar_curso', args=[self.request.POST['curso_id']]) + '?correcto=ok'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = curso.objects.get(id=self.request.GET['curso_id'])
        context['titulo_template'] = 'Edicion de alcance'
        context['titulo'] = context['curso'].titulo

        return context


class RecomendacionDeleteView(DeleteView):
    model = recomendacion

    # success_url = reverse_lazy('visitante:en_preparacion')

    def get_success_url(self):
        return reverse_lazy('visitante:editar_curso', args=[self.request.GET['curso_id']]) + '?correcto=ok'


class CapituloCreateView(CreateView):
    model = capitulo
    form_class = CapituloForm
    template_name = 'visitante/capitulo_form.html'

    def get_success_url(self, *args):
        return reverse_lazy('visitante:editar_curso', args=[args[0].id]) + '?correcto=ok'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        curso_post = curso.objects.get(id=request.POST['curso_id'])
        if form.is_valid():
            el_capitulo = form.save(commit=False)
            el_capitulo.curso = curso_post
            el_capitulo.save()
            return HttpResponseRedirect(self.get_success_url(curso_post))
        return render(request, 'visitante/capitulo_form.html', {'form': form, 'curso': curso_post})

    def get_context_data(self, **kwargs):
        context = super(CapituloCreateView, self).get_context_data(**kwargs)
        context['curso'] = curso.objects.get(id=self.request.GET['curso_id'])
        context['titulo_template'] = 'Nuevo Capitulo'
        context['titulo'] = context['curso'].titulo
        return context


class CapituloUpdateView(UpdateView):
    model = capitulo
    form_class = CapituloForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        el_curso = self.object.curso
        return reverse_lazy('visitante:editar_curso', args=[el_curso.id]) + '?correcto=ok'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = self.object.curso
        context['titulo_template'] = 'Edicion de capitulo'
        context['titulo'] = context['curso'].titulo
        # Lista de capitulos
        context['lista_temas'] = tema.objects.filter(capitulo=self.object)
        return context


class CapituloDeleteView(DeleteView):
    model = capitulo

    # success_url = reverse_lazy('visitante:en_preparacion')

    def get_success_url(self):
        el_curso = self.object.curso
        return reverse_lazy('visitante:editar_curso', args=[el_curso.id]) + '?correcto=ok'


class TemaCreateView(CreateView):
    model = tema
    form_class = TemaForm
    template_name = 'visitante/tema_form.html'

    def get_success_url(self, *args):
        return reverse_lazy('visitante:editar_capitulo', args=[args[0].id]) + '?curso_id=' + str(
            args[0].curso.id) + '&correcto=ok'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        capitulo_post = capitulo.objects.get(id=request.POST['capitulo_id'])
        if form.is_valid():
            el_tema = form.save(commit=False)
            el_tema.capitulo = capitulo_post
            el_tema.save()
            return HttpResponseRedirect(self.get_success_url(capitulo_post))
        else:
            return render(request, 'visitante/tema_form.html', {'form': form, 'capitulo': capitulo_post})

    def get_context_data(self, **kwargs):
        context = super(TemaCreateView, self).get_context_data(**kwargs)
        context['capitulo'] = capitulo.objects.get(id=self.request.GET['capitulo_id'])
        context['titulo_template'] = 'Nuevo Tema'
        context['titulo'] = str(context['capitulo'].nombre) + ' ' + str(context['capitulo'].curso.titulo)
        return context


class TemaUpdateView(UpdateView):
    model = tema
    form_class = TemaForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        capitulo_post = capitulo.objects.get(id=self.request.POST['capitulo_id'])
        return reverse_lazy('visitante:editar_capitulo', args=[capitulo_post.id]) + '?curso_id=' + str(
            capitulo_post.curso.id) + '&correcto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['capitulo'] = capitulo.objects.get(id=self.request.GET['capitulo_id'])
        context['titulo_template'] = 'Edicion del Tema'
        context['titulo'] = context['capitulo'].nombre
        # Lista de detalles
        # context['lista_detalles'] = detalle.objects.filter(tema=self.object)
        lista = []
        for obj in detalle.objects.filter(tema=self.object):
            if obj.imagen != '':
                lista.append([obj, 'imagen'])
            elif obj.media != '':
                lista.append([obj, 'media'])
            elif obj.texto != '':
                lista.append([obj, 'texto'])
            else:
                lista.append([obj, ''])
        context['lista_detalles'] = lista
        return context


class TemaDeleteView(DeleteView):
    model = tema

    # success_url = reverse_lazy('visitante:en_preparacion')

    def get_success_url(self):
        curso_id = capitulo.objects.get(id=self.request.GET['capitulo_id']).curso.id
        return reverse_lazy('visitante:editar_capitulo', args=[self.request.GET['capitulo_id']]) + '?curso_id=' + str(
            curso_id) + '&correcto=ok'


class DetalleCreateView(CreateView):
    model = detalle
    form_class = DetalleForm
    template_name = 'visitante/detalle_form.html'

    def get_success_url(self, *args):
        return reverse_lazy('visitante:editar_tema', args=[args[0].id]) + '?capitulo_id=' + str(
            args[0].capitulo.id) + '&correcto=ok'

    def post(self, request, *args, **kwargs):
        videos = ['.mp4', '.ogv', '.webM']
        audios = ['.mp3', '.wav']
        textos = ['.txt', '.odt', '.docs', '.pdf']
        form = self.form_class(request.POST, request.FILES)
        tema_post = tema.objects.get(id=request.POST['tema_id'])
        if form.is_valid():
            nombre = request.FILES.get('media')
            el_detalle = form.save(commit=False)
            el_detalle.nombrearchivo = nombre
            # nombre, extension = os.path.splitext(os.getcwd() + '/media/visitante/' + str(nombre))
            extension = os.path.splitext(os.getcwd() + '/media/visitante/' + str(nombre))[1]
            # videos
            for tipo in videos:
                if tipo == extension:
                    el_detalle.tipoarchivo = 'v'
                    break
            # audios
            for tipo in audios:
                if tipo == extension:
                    el_detalle.tipoarchivo = 'a'
                    break
            # textos
            for tipo in textos:
                if tipo == extension:
                    el_detalle.tipoarchivo = 't'
                    break
            if el_detalle.tipoarchivo == 'n':
                el_detalle.media = None
                el_detalle.nombrearchivo = ''

            el_detalle.tema = tema_post
            el_detalle.save()
            return HttpResponseRedirect(self.get_success_url(tema_post))
        else:
            return render(request, 'visitante/tema_form.html', {'form': form, 'tema': tema_post})

    def get_context_data(self, **kwargs):
        context = super(DetalleCreateView, self).get_context_data(**kwargs)
        context['tema'] = tema.objects.get(id=self.request.GET['tema_id'])
        context['titulo_template'] = 'Nuevo Detalle'
        context['titulo'] = str(context['tema'].nombre)
        return context


class DetalleUpdateView(UpdateView):
    model = detalle
    form_class = DetalleForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        el_tema = tema.objects.get(id=self.request.POST['tema_id'])
        return reverse_lazy('visitante:editar_tema', args=[el_tema.id]) + '?capitulo_id=' + str(
            el_tema.capitulo.id) + '&correcto=ok'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        el_tema = tema.objects.get(id=self.request.GET['tema_id'])
        context['tema'] = el_tema
        context['titulo_template'] = 'Edicion del Tema'
        context['titulo'] = el_tema.nombre + ' ' + el_tema.capitulo.nombre

        return context

    def post(self, request, *args, **kwargs):
        videos = ['.mp4', '.ogv', '.webM']
        audios = ['.mp3', '.wav']
        textos = ['.txt', '.odt', '.docs', '.pdf']
        self.object = self.get_object()
        form = self.get_form()
        mi_detalle = form.save(commit=False)
        nombre = request.FILES.get('media')
        mi_detalle.nombrearchivo = nombre
        # nombre, extension = os.path.splitext(os.getcwd() + '/media/visitante/' + str(nombre))
        extension = os.path.splitext(os.getcwd() + '/media/visitante/' + str(nombre))[1]
        # videos
        for tipo in videos:
            if tipo == extension:
                mi_detalle.tipoarchivo = 'v'
                break
        # audios
        for tipo in audios:
            if tipo == extension:
                mi_detalle.tipoarchivo = 'a'
                break
        # textos
        for tipo in textos:
            if tipo == extension:
                mi_detalle.tipoarchivo = 't'
                break
        if mi_detalle.tipoarchivo == 'n':
            mi_detalle.media = None
            mi_detalle.nombrearchivo = ''
        mi_detalle.save()
        return HttpResponseRedirect(self.get_success_url())


class DetalleDeleteView(DeleteView):
    model = detalle

    # success_url = reverse_lazy('visitante:en_preparacion')

    def get_success_url(self):
        el_tema = tema.objects.get(id=self.request.GET['tema_id'])
        return reverse_lazy('visitante:editar_tema', args=[el_tema.id]) + '?capitulo_id=' + str(
            el_tema.capitulo.id) + '&correcto=ok'
