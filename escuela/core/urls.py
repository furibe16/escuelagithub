from django.contrib import admin
from django.urls import path, include
from core.views import cursos, NuevoCursoView, ListaCursosBusquedaView, EnPreparacionView, \
    EditarCursoView, BorrarCursoView, DisciplinaListView, DisciplinaCreateView, DisciplinaUpdateView, \
    DisciplinaDeleteView, InscripcionView, EstudioView, ConstruidoView

core_patterns = ([

                     path('', cursos.as_view(), name="home"),
                     path('NuevoCurso/', NuevoCursoView, name='nuevo_curso'),
                     path('lista_cursos_busqueda/', ListaCursosBusquedaView, name='lista_cursos_busqueda'),
                     path('en_preparacion/', EnPreparacionView, name='en_preparacion'),
                     path('editar_curso/<int:pk>/', EditarCursoView, name='editar_curso'),
                     path('borrar_curso/<int:pk>/', BorrarCursoView, name='borrar_curso'),
                     path('lista_disciplinas/', DisciplinaListView.as_view(), name='lista_disciplinas'),
                     path('nueva_disciplina/', DisciplinaCreateView.as_view(), name='nueva_disciplina'),
                     path('editar_disciplina/<int:pk>/', DisciplinaUpdateView.as_view(), name='editar_disciplina'),
                     path('borrar_disciplina/<int:pk>/', DisciplinaDeleteView.as_view(), name='borrar_disciplina'),
                     path('inscripcion/<int:curso>/', InscripcionView, name='inscripcion'),
                     path('estudio/<int:curso>/', EstudioView, name='estudio'),
                     path('construido/', ConstruidoView, name='construido'),

                 ], "core")
