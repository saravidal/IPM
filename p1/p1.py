"""
	IPM - CURSO 2016/17
	
	SPRINT 3
	
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

	Crea la lista de peliculas, los botones de la ventana principal
	(Add, Delete y Edit) y el desplegable que permite mostrar todas 
	las peliculas, solo las vistas o solo las que aun no se han visto.
"""
class MovieModel():
	
	def __init__(self, controller):
		
		#Creamos un arbol
		self.moviesList = Gtk.ListStore(str, bool) #True = pelicula vista
		
		#Creamos los botones
		self.buttons = list()
		for acciones in [_("Add"), _("Delete"), _("Edit")]:
			self.button = Gtk.Button(acciones)
			self.buttons.append(self.button)
			self.button.connect("clicked", controller.on_selection_button_clicked)

		#Creamos las opciones del menu desplegable de visualizado de las peliculas
		showm = Gtk.ListStore(str)
		showm.append([_("Show all movies")])
		showm.append([_("Show watched movies")])
		showm.append([_("Show unwatched movies")])
		self.show_combo = Gtk.ComboBox.new_with_model(showm)
		self.show_combo.set_active(0)
		self.show_combo.connect("changed", controller.on_show_combo_changed)
		renderer_text = Gtk.CellRendererText()
		self.show_combo.pack_start(renderer_text, True)
		self.show_combo.add_attribute(renderer_text, "text", 0)


""" EntryModel

	Crea la entrada de texto, los botones de la ventana para anadir
	(Add y Cancel) o editar una pelicula (Edit y Cancel) y el checkbutton
	para indicar si una pelicula se ha visto o no.
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
		
		#Creamos el checkbutton
		self.checkwatched = Gtk.CheckButton(_("I've watched this movie"))


#-----------------------------------------------------------------------

""" MovieView

	Vista de la ventana principal (lista de peliculas (con el filtro 
	para visualizar todas, las vistas o las no vistas), botones Add,
	Delete y Edit, y menu desplegable para decidir que peliculas 
	mostrar).
"""
class MovieView(Gtk.Window):
	
	def __init__(self,controller):
		
		Gtk.Window.__init__(self, title = _("Movies"))
		self.set_border_width(10)
		self.iter = Gtk.TreeIter()
		
		#Creamos el grid
		self.grid = Gtk.Grid()
		self.grid.set_row_homogeneous(True)
		self.grid.set_column_homogeneous(True)
		self.add(self.grid)
		
		#Creamos el filtro	
		self.current_filter_watched = None
		self.watched_filter = controller.model.moviesList.filter_new()
		self.watched_filter.set_visible_func(controller.watched_filter_func)
		
		#Creamos el treeview
		self.treeview = Gtk.TreeView.new_with_model(self.watched_filter)
		for i, column_title in enumerate([_("Movies")]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text = i)
			self.treeview.append_column(column)
			
		#Creamos el scroll y lo colocamos en el grid
		self.scroll = Gtk.ScrolledWindow()
		self.scroll.set_vexpand(True)
		self.grid.attach(self.scroll, 0, 0, 4, 10)
		
		#Creamos el menu desplegable y lo colocamos en el grid
		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.vbox.pack_start(controller.model.show_combo, False, False, True)
		self.grid.attach_next_to(self.vbox, self.scroll, Gtk.PositionType.BOTTOM, 1, 1)
		
		#Colocamos los botones en el grid
		self.grid.attach_next_to(controller.model.buttons[0], self.vbox, Gtk.PositionType.RIGHT, 1, 1)
		for i, button in enumerate(controller.model.buttons[1:]):
			self.grid.attach_next_to(button, controller.model.buttons[i], Gtk.PositionType.RIGHT, 1, 1)

		#Colocamos el treeview en el grid
		self.scroll.add(self.treeview)
		
		self.show_all()
			
	
""" EntryView

	Vista de la ventana de entrada de texto, con la entrada de texto y
	los botones Add y Cancel para el caso de anadir pelicula y los
	botones Edit y Cancel para el caso de editar pelicula, y el checkbutton
	para indicar si una pelicula ha sido vista o no.
"""	
class EntryView(Gtk.Window):	

	def __init__(self, controller):
		
		Gtk.Window.__init__(self, title = controller.button_recv)
		self.set_border_width(10)
	
		self.table = Gtk.Table(2,3)

		self.table.attach(controller.entrymodel.entry, 0, 1, 0, 1)
		self.table.attach(controller.entrymodel.bok, 1, 2, 0, 1)
		self.table.attach(controller.entrymodel.bcancel, 2, 3, 0, 1)
		self.table.attach(controller.entrymodel.checkwatched, 0,1,1,2)
		
		self.add(self.table)
		
		
		self.show_all()
		
		
#-----------------------------------------------------------------------

""" DialogNoMovie

	Dialogo que se crea cuando se pulsa Delete o Edit en la ventana
	principal bajo alguna de las siguientes condiciones:
	-No hay ninguna pelicula en la lista: mensaje "No movies yet"
	-No hay ninguna pelicula de la lista seleccionada: mensaje "Please,
	select a movie"
	O cuando se trata de anadir una pelicula que ya existe o editar una
	y cambiarle los valores a otros de una pelicula que ya existe:
	mensaje "This movie already exists"
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
	Controla el filtro de peliculas.
	Controla el menu desplegable.
"""
class MovieController():
	
	#Inicializacion
	def __init__(self):
		self.model = MovieModel(self)
		self.view = MovieView(self)
		self.view.connect("delete_event", Gtk.main_quit)
		self.view.show_all()

	#Funcionamiento de los botones
	def on_selection_button_clicked(self, button):
		
		self.button_recv = button.get_label()
		
		if self.button_recv == _("Add"):
			self.entrymodel = EntryModel(self)
			self.entryview = EntryView(self)
			
		elif (self.button_recv == _("Delete")) or (self.button_recv == _("Edit")):
			self.selectedaction()
			
		elif self.button_recv == _("Add "):
			movie = self.entrymodel.entry.get_text()
			watched = self.entrymodel.checkwatched.get_active()
			if self.scrollthroughlist(movie,watched):
				self.dialog = DialogNoMovie(self.view, _("This movie already exists"))
				self.dialog.run()
				self.dialog.destroy()
			else:
				self.model.moviesList.append([movie,watched])
				self.entryview.destroy()
			
		elif self.button_recv == _("Edit "):
			movie = self.entrymodel.entry.get_text()
			watched = self.entrymodel.checkwatched.get_active()
			iter = self.view.iter
			if self.scrollthroughlist(movie,watched):
				self.dialog = DialogNoMovie(self.view, _("This movie already exists"))
				self.dialog.run()
				self.dialog.destroy()
			else:
				self.view.iter = iter
				self.model.moviesList.insert_after(self.view.iter,[movie,watched])
				self.model.moviesList.remove(self.view.iter)
				self.entryview.destroy()
		
		elif self.button_recv == _("Cancel"):
			self.entryview.destroy()
			
			
	#Funcionamiento del filtro		
	def watched_filter_func(self, model, iter, data):
		if self.view.current_filter_watched is None or self.view.current_filter_watched == "None":
			return True
		else:
			return model[iter][1] == self.view.current_filter_watched
		
		
	#Funcionamiento del menu desplegable	
	def on_show_combo_changed(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter != None:
			combo_recv = combo.get_model()
			if combo_recv[tree_iter][0]	== _("Show all movies"):
				self.view.current_filter_watched = None
			elif combo_recv[tree_iter][0] == _("Show watched movies"):
				self.view.current_filter_watched = True
			elif combo_recv[tree_iter][0] == _("Show unwatched movies"):	
				self.view.current_filter_watched = False
			self.view.watched_filter.refilter()
			
			
	#Funcion que recorre la lista de peliculas buscando una pelicula dada					
	def scrollthroughlist(self, movie, watched):
		self.view.iter = self.model.moviesList.get_iter_first()
		i = 0
		while i < len(self.model.moviesList):
			if (self.model.moviesList.get_value(self.view.iter,0) == movie) and \
			(self.model.moviesList.get_value(self.view.iter,1) == watched):
				return True
			else:
				self.view.iter = self.model.moviesList.iter_next(self.view.iter)
			i = i+1
		return False
		
			
	#Funcion que lanza los dialogos de Edit y Cancel o ejecuta sus acciones		
	def	selectedaction(self):
		
		if len(self.model.moviesList) == 0:
			self.dialog = DialogNoMovie(self.view, _("No movies yet"))
			self.dialog.run()
			self.dialog.destroy()
		else:
			self.treeselection = self.view.treeview.get_selection()
			self.treeselection.set_mode(Gtk.SelectionMode.SINGLE)
			(aux, iter) = self.treeselection.get_selected()		
			if iter is None:
				self.dialog = DialogNoMovie(self.view, _("Please, select a movie"))
				self.dialog.run()
				self.dialog.destroy()
			else:
				movie = aux.get_value(iter,0)
				watched = aux.get_value(iter,1)
				if self.scrollthroughlist(movie,watched):
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
