"""
	IPM - CURSO 2016/17
	
	SPRINT 2
	
	VIDAL GARCIA, SARA
	GARCIA SANCHEZ, JOSE LUIS
	
	GRUPO 3.3
	
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import gettext
try:
	lang = gettext.translation('p1', localedir='./locale')
	lang.install()
except:
	_ = lambda s: s

#-----------------------------------------------------------------------

""" MovieModel

	Crea la lista de peliculas y los botones de la ventana principal
	(Add, Delete y Edit).
"""
class MovieModel():
	
	def __init__(self, controller):
		
		#Creamos un arbol
		self.moviesList = Gtk.ListStore(str)
		
		#Creamos los botones
		self.buttons = list()
		for acciones in [_("Add"), _("Delete"), _("Edit")]:
			self.button = Gtk.Button(acciones)
			self.buttons.append(self.button)
			self.button.connect("clicked", controller.on_selection_button_clicked)
		

""" EntryModel

	Crea la entrada de texto y los botones de la ventana para anadir
	(Add y Cancel) o editar una pelicula (Edit y Cancel).
"""
class EntryModel():
	
	def __init__(self,controller):

		#Creamos el campo para introducir el nombre
		self.entry = Gtk.Entry()
		if controller.button_recv == _("Add"):
			self.entry.set_text(_("Name of the movie"))
		else:
			self.entry.set_text(controller.model.moviesList[controller.view.iter][0])
		
		#Creamos los botones
		if controller.button_recv == _("Add"):
			self.bok = Gtk.Button(_("Add "))
		else:
			self.bok = Gtk.Button(_("Edit "))
		self.bcancel = Gtk.Button(_("Cancel"))
		self.bok.connect("clicked", controller.on_selection_button_clicked)
		self.bcancel.connect("clicked", controller.on_selection_button_clicked)

#-----------------------------------------------------------------------

""" MovieView

	Vista de la ventana principal (lista de peliculas y botones Add,
	Delete y Edit.
"""
class MovieView(Gtk.Window):
	
	def __init__(self,controller):
		
		Gtk.Window.__init__(self, title = _("Movies"))
		self.set_border_width(10)
		self.iter = Gtk.TreeIter()
		
		self.grid = Gtk.Grid()
		self.grid.set_column_homogeneous(True)
		self.grid.set_row_homogeneous(True)
		self.add(self.grid)
		
		self.treeview = Gtk.TreeView(controller.model.moviesList)
		for i, column_title in enumerate([_("Movies")]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text = i)
			self.treeview.append_column(column)
	
		self.scroll = Gtk.ScrolledWindow()
		self.scroll.set_vexpand(True)
		self.grid.attach(self.scroll, 0, 0, 8, 10)
		self.grid.attach_next_to(controller.model.buttons[0], self.scroll, Gtk.PositionType.BOTTOM, 1, 1)
		
		for i, button in enumerate(controller.model.buttons[1:]):
			self.grid.attach_next_to(button, controller.model.buttons[i], Gtk.PositionType.RIGHT, 1, 1)
		self.scroll.add(self.treeview)
		
		self.show_all()
	
	
""" EntryView

	Vista de la ventana de entrada de texto, con la entrada de texto y
	los botones Add y Cancel para el caso de anadir pelicula y los
	botones Edit y Cancel para el caso de editar pelicula.
"""	
class EntryView(Gtk.Window):	

	def __init__(self, controller):
		
		Gtk.Window.__init__(self, title = controller.button_recv)
		self.set_border_width(10)
	
		self.table = Gtk.Table(1,3)

		self.table.attach(controller.entrymodel.entry, 0, 1, 0, 1)
		self.table.attach(controller.entrymodel.bok, 1, 2, 0, 1)
		self.table.attach(controller.entrymodel.bcancel, 2, 3, 0, 1)
		self.add(self.table)
		
		self.show_all()
		
#-----------------------------------------------------------------------

""" DialogNoMovie

	Dialogo que se crea cuando se pulsa Delete o Edit en la ventana
	principal bajo alguna de las siguientes condiciones:
	-No hay ninguna pelicula en la lista: mensaje "No movies yet"
	-No hay ninguna pelicula de la lista seleccionada: mensaje "Please,
	select a movie"
"""
class DialogNoMovie(Gtk.Dialog):

    def __init__(self, parent, dialogtext):
        Gtk.Dialog.__init__(self, _("ERROR"), parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)
		
        label = Gtk.Label(dialogtext)

        box = self.get_content_area()
        box.add(label)
        self.show_all()


""" DialogAreyousure
	
	Dialogo que se crea cuando un usuario intenta borrar una pelicula
	de la lista, con el mensaje "This movie will be deleted. Are you
	sure?"
"""
class DialogAreyousure(Gtk.Dialog):
	
	def __init__(self, parent):
		Gtk.Dialog.__init__(self, _("WARNING"), parent, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
		
		self.set_default_size(150, 100)
		
		label = Gtk.Label(_("This movie will be deleted. Are you sure?"))
		
		box = self.get_content_area()
		box.add(label)
		self.show_all()


#-----------------------------------------------------------------------

""" MovieController

	Controlador de la aplicacion.
	Inicia el modelo y la vista de la ventana principal.
	Controla las acciones de todos los botones.
	Lanza los dialogos.
"""
class MovieController():
	
	def __init__(self):
		self.model = MovieModel(self)
		self.view = MovieView(self)
		self.view.connect("delete_event", Gtk.main_quit)
		self.view.show_all()


	def on_selection_button_clicked(self, button):
		
		self.button_recv = button.get_label()
		
		if self.button_recv == _("Add"):
			self.entrymodel = EntryModel(self)
			self.entryview = EntryView(self)
			
		elif (self.button_recv == _("Delete")) or (self.button_recv == _("Edit")):
			self.selectedaction()
			
		elif self.button_recv == _("Add "):
			self.model.moviesList.append([self.entrymodel.entry.get_text()])
			self.entryview.destroy()
			
		elif self.button_recv == _("Edit "):
			self.model.moviesList.insert_after(self.view.iter, [self.entrymodel.entry.get_text()])
			self.model.moviesList.remove(self.view.iter)
			self.entryview.destroy()
		
		elif self.button_recv == _("Cancel"):
			self.entryview.destroy()
			
			
	def	selectedaction(self):
		
		if len(self.model.moviesList) == 0:
			self.dialog = DialogNoMovie(self.view, _("No movies yet"))
			self.dialog.run()
			self.dialog.destroy()
		else:
			self.treeselection = self.view.treeview.get_selection()
			self.treeselection.set_mode(Gtk.SelectionMode.SINGLE)
			(self.model.movieslist, self.view.iter) = self.treeselection.get_selected()
			if self.view.iter is None:
				self.dialog = DialogNoMovie(self.view, _("Please, select a movie"))
				self.dialog.run()
				self.dialog.destroy()
			else:
				if self.button_recv == _("Delete"):
					dialog = DialogAreyousure(self.view)
					response = dialog.run()
					if response == Gtk.ResponseType.OK:
						self.model.moviesList.remove(self.view.iter)
					dialog.destroy()
				else:
					self.entrymodel = EntryModel(self)
					self.entryview = EntryView(self)
			
#-----------------------------------------------------------------------

c = MovieController()
Gtk.main()
