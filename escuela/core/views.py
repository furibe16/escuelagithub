from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, CreateView, UpdateView, DeleteView

from core.forms import CursoForm, DisciplinaForm
from core.models import curso, disciplina, inscripcion
from django.contrib.auth.models import AnonymousUser
from registration.models import perfil
from visitante.models import capitulo, tema, detalle


def NuevoCursoView(request):
    titulo_template = "Nuevo Curso"
    mensaje = 'Esta es la etapa inicial'

    form = CursoForm()
    if request.method == 'POST':
        mensaje = 'Todo fue exitoso'
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_curso = form.save(commit=False)
            nuevo_curso.profesor = request.user.username
            nuevo_curso.save()
            # Vuelve al amigo, profesor
            usuario = request.user
            if usuario.first_name == 'm':
                usuario.first_name = 'p'
            elif usuario.first_name == 'a':
                usuario.first_name = 'b'
            usuario.save()
            return HttpResponseRedirect(reverse('core:home'))
        else:
            mensaje = "Ha ocurrido un error"

    return render(request, 'curso.html', {'form': form, 'mensaje': mensaje, 'titulo_template': titulo_template})


class cursos(FormView):
    # busca los ultimos cursos creados y los mejores cursos gratuitos
    def get(self, *args, **kwargs):
        # lista_ultimos = curso.objects.filter(completo=True).order_by('created').reverse()[0:5] ** todos los cursos
        lista_ultimos = curso.objects.filter(completo=True).order_by('created').reverse()[0:5]
        mejores_gratuitos = curso.objects.filter(precio=0, completo=True).order_by('alumnos').reverse()[0:5]
        return render(self.request, "home.html", {"lista": lista_ultimos, "mejores_gratuitos": mejores_gratuitos})


def ListaCursosBusquedaView(request):
    criterio = request.GET['criterio']
    lista = None
    if criterio == '*':
        lista = curso.objects.all()
    elif criterio != '':
        lista = curso.objects.filter(titulo__icontains=criterio) | curso.objects.filter(descripcion__icontains=criterio)
    return render(request, 'lista_cursos_busqueda.html', {'lista': lista})


def EnPreparacionView(request):
    lista = None
    lista = curso.objects.filter(completo=False, profesor=request.user)
    return render(request, 'en_preparacion.html', {'lista': lista})


def EditarCursoView(request, pk):
    mensaje = ''
    curso1 = curso.objects.get(id=pk)
    titulo_template = "Edicion de Curso"
    titulo = curso1.titulo
    form = CursoForm(instance=curso1)
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES, instance=curso1)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('core:en_preparacion'))
        else:
            mensaje = "Ha ocurrido un error"
    return render(request, 'curso.html',
                  {'form': form, 'mensaje': mensaje, 'titulo_template': titulo_template, 'titulo': titulo})


def BorrarCursoView(request, pk):
    curso1 = curso.objects.get(id=pk)
    curso1.delete()
    return HttpResponseRedirect(reverse('core:en_preparacion'))


def InscripcionView(request, **kwargs):
    user = request.user
    if kwargs['curso'] > 0:
        mi_curso = curso.objects.get(id=kwargs['curso'])
        # Busca si esta ya inscrito
        lista = inscripcion.objects.filter(curso=mi_curso, alumno=user)
        if lista.count() == 0:
            mi_nscripcion = inscripcion()
            mi_nscripcion.alumno = user
            mi_nscripcion.curso = mi_curso
            mi_nscripcion.save()
            mi_curso.alumnos += 1
            mi_curso.save()
            if user.first_name == 'p':
                user.first_name = 'b'
            else:
                user.first_name = 'a'
            user.save()
            # Obtiene el perfil
            mi_perfil = perfil.objects.get(user=user)
            mi_perfil.alumno = True
            mi_perfil.save()

    lista = inscripcion.objects.filter(alumno=user)
    return render(request, 'core/inscripcion_lista.html', {'lista_inscripciones': lista})


def EstudioView(request, **kwargs):
    mi_curso = curso.objects.get(id=kwargs['curso'])
    capitulos = []
    temas = []
    detalles = []

    for cap in capitulo.objects.filter(curso=mi_curso):
        capitulos.append(cap)
        for tem in tema.objects.filter(capitulo=cap):
            temas.append(tem)
            for det in detalle.objects.filter(tema=tem):
                detalles.append(det)

    contenido = []
    for cap in capitulo.objects.filter(curso=mi_curso):
        contenido.append([cap, 'capitulo'])
        for tem in tema.objects.filter(capitulo=cap):
            contenido.append([tem, 'tema'])
            for det in detalle.objects.filter(tema=tem):
                contenido.append([det, 'detalle'])

    return render(request, 'core/estudio.html',
                  {'capitulos': capitulos, 'temas': temas, 'detalles': detalles, 'curso': mi_curso,
                   'contenido': contenido})


def ConstruidoView(request):
    usuario = request.user
    lista = curso.objects.filter(profesor=usuario, completo=True)
    return render(request, 'core/construido.html', {'lista': lista, 'ingresos': 12.34})


class DisciplinaListView(ListView):
    model = disciplina

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista = disciplina.objects.all()
        context['lista'] = lista
        return context


class DisciplinaCreateView(CreateView):
    model = disciplina
    form_class = DisciplinaForm
    template_name = "core/disciplina_form.html"
    success_url = reverse_lazy('core:lista_disciplinas')

    """def get_success_url(self):
        return reverse_lazy('core:lista_disciplinas')"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_template'] = 'Registro de una Disciplina'
        return context


class DisciplinaUpdateView(UpdateView):
    model = disciplina
    form_class = DisciplinaForm
    # template_name_suffix = '_form'
    template_name = "core/disciplina_form.html"
    success_url = reverse_lazy('core:lista_disciplinas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        disciplina1 = self.object
        context['titulo_template'] = 'Edicion de: '
        context['titulo'] = disciplina1.nombre
        return context


class DisciplinaDeleteView(DeleteView):
    model = disciplina
    success_url = reverse_lazy('core:lista_disciplinas')
