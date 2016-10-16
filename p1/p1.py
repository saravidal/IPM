"""
	IPM - CURSO 2016/17
	
	SPRINT 5
	
	VIDAL GARCIA, SARA
	GARCIA SANCHEZ, JOSE LUIS
	
	GRUPO 3.3
	
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Idiomas
import gettext, locale
try:
	lang = gettext.translation('p1', localedir='./locale')
	lang.install()
except:
	_ = lambda s: s


# Uso de themoviedb para recomendaciones:
import requests, json
KEY = "25d91d617b990e4a14ee567b42838ea3" #Cada usuario debe introducir su key


#Para evitar errores en comparaciones de strings con tildes
import unicodedata


#-----------------------------------------------------------------------

""" MovieModel

------------------------------------------------------------------------
	
	Descripcion:
	
	Crea la lista de peliculas, los botones de la ventana principal
	(Add, Delete y Edit) y el desplegable que permite mostrar todas 
	las peliculas, solo las vistas, solo las que aun no se han visto
	o las recomendaciones.
	
------------------------------------------------------------------------

	Atributos:
	
	self.moviesList: Lista de peliculas. Tiene dos campos, el primero almacena
	el titulo de la pelicula y el segundo la clasifica:
		w: vista
		u: no vista
		r: recomendada
	
	self.buttons: Lista de botones de la ventana principal:
		Add
		Delete
		Edit

	self.show_combo: Menu desplegable con las opciones:
		Mostrar todas las peliculas
		Mostrar solo las peliculas vistas
		Mostrar solo las peliculas no vistas
		Mostrar las recomendaciones
	
	
	action: iterador
	
	button: para crear los botones
	
	show_options: para almacenar las opciones del menu desplegable

	renderer_text: para renderizar el texto del menu desplegable
	
"""
class MovieModel():
	
	def __init__(self, controller):		

		self.moviesList = Gtk.ListStore(str, str)

		
		self.buttons = list()
		for action in [_("Add"), _("Delete"), _("Edit")]:
			button = Gtk.Button(action)
			self.buttons.append(button)
			button.connect("clicked", controller.on_selection_button_clicked)


		show_options = Gtk.ListStore(str)
		
		for action in [_("Show all movies"),_("Show watched movies"),_("Show unwatched movies"),_("Show recommendations")]:
			show_options.append([action])

		self.show_combo = Gtk.ComboBox.new_with_model(show_options)
		self.show_combo.set_active(0)
		self.show_combo.connect("changed", controller.on_show_combo_changed)
		renderer_text = Gtk.CellRendererText()
		self.show_combo.pack_start(renderer_text, True)
		self.show_combo.add_attribute(renderer_text, "text", 0)



""" EntryModel

------------------------------------------------------------------------

	Descripcion:
	
	Crea la entrada de texto, los botones de la ventana para anadir
	(Add y Cancel) o editar una pelicula (Edit y Cancel) y el checkbutton
	para indicar si una pelicula se ha visto o no.

------------------------------------------------------------------------

	Atributos:

	self.entry: Entrada de texto para introducir el titulo de la pelicula,
	con el texto por defecto "Name of the movie" en el caso de anadir una
	pelicula, o el nombre de la pelicula en el caso de editar una pelicula
	
	self.oldmovie: Titulo de la pelicula antes de que esta sea modificada
	
	self.bok: Boton Add en el caso de Add / Boton Edit en el caso de Edit
	
	self.bcancel: Boton Cancel
	
	self.checkwatched: Checkbutton para indicar si una pelicula se ha visto
	


"""
class EntryModel():
	
	def __init__(self,controller):

		
		self.entry = Gtk.Entry()
		
		if controller.button_recv == _("Add"):
			self.entry.set_text(_("Name of the movie"))
			self.bok = Gtk.Button(_("Add "))
		
		else:
			self.oldmovie = controller.model.moviesList[controller.view.iter][0]
			self.entry.set_text(self.oldmovie)
			self.bok = Gtk.Button(_("Edit "))
		
		self.bcancel = Gtk.Button(_("Cancel"))
		
		self.bok.connect("clicked", controller.on_selection_button_clicked)
		self.bcancel.connect("clicked", controller.on_selection_button_clicked)

		self.checkwatched = Gtk.CheckButton(_("I've watched this movie"))



#-----------------------------------------------------------------------

""" MovieView

------------------------------------------------------------------------

	Descripcion:
	
	Vista de la ventana principal (lista de peliculas (con el filtro 
	para visualizar todas, las vistas, las no vistas o las recomendadas), 
	botones Add, Delete y Edit, y menu desplegable para decidir que 
	peliculas mostrar).
	
------------------------------------------------------------------------

	Atributos:
	
	self.iter: Iterador que recorre la lista de peliculas
	
	self.current_filter_watched: Estado actual del filtro
	
	self.watched_filter: Filtro para decidir que peliculas mostrar
	
	self.treeview: Vista de la lista de peliculas con el filtro aplicado
	
	
	grid: parrilla en la que se disponen todos los elementos de la
		  ventana principal
		  
	renderer: para renderizar texto
	
	column: para obtener una columna	  
	
	scroll: ventana de scroll para la visualizacion de las peliculas
	
	vbox: caja en la que colocar el menu desplegable
	
	i, button: iteradores
	
"""
class MovieView(Gtk.Window):
	
	def __init__(self,controller):

		
		Gtk.Window.__init__(self, title = _("Movies"))
		self.set_border_width(10)
		self.iter = Gtk.TreeIter()
		
	
		grid = Gtk.Grid()
		grid.set_row_homogeneous(True)
		grid.set_column_homogeneous(True)
		self.add(grid)
		
		
		self.current_filter_watched = None
		self.watched_filter = controller.model.moviesList.filter_new()
		self.watched_filter.set_visible_func(controller.watched_filter_func)
		
		
		self.treeview = Gtk.TreeView.new_with_model(self.watched_filter)
		
		for i, column_title in enumerate([_("Movies")]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text = i)
			self.treeview.append_column(column)
			
		
		scroll = Gtk.ScrolledWindow()
		scroll.set_vexpand(True)
		grid.attach(scroll, 0, 0, 5, 10)
		
		
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		vbox.pack_start(controller.model.show_combo, False, False, True)
		grid.attach_next_to(vbox, scroll, Gtk.PositionType.BOTTOM, 2, 1)
		
		
		grid.attach_next_to(controller.model.buttons[0], vbox, Gtk.PositionType.RIGHT, 1, 1)
		
		for i, button in enumerate(controller.model.buttons[1:]):
			grid.attach_next_to(button, controller.model.buttons[i], Gtk.PositionType.RIGHT, 1, 1)

		
		scroll.add(self.treeview)
		
		self.show_all()
			
	
	
""" EntryView

------------------------------------------------------------------------

	Descripcion:
	Vista de la ventana de entrada de texto, con la entrada de texto y
	los botones Add y Cancel para el caso de anadir pelicula y los
	botones Edit y Cancel para el caso de editar pelicula, y el checkbutton
	para indicar si una pelicula ha sido vista o no.
	
------------------------------------------------------------------------

	Atributos:

	
	table: tabla en la que disponer los elementos de la ventana
	
"""	
class EntryView(Gtk.Window):	

	def __init__(self, controller):
	
		
		Gtk.Window.__init__(self, title = controller.button_recv)
		self.set_border_width(10)
		

		table = Gtk.Table(2,3)


		table.attach(controller.entrymodel.entry, 0, 1, 0, 1)
		table.attach(controller.entrymodel.bok, 1, 2, 0, 1)
		table.attach(controller.entrymodel.bcancel, 2, 3, 0, 1)
		table.attach(controller.entrymodel.checkwatched, 0,1,1,2)
		
		self.add(table)
		
		
		self.show_all()
		
		
		
#-----------------------------------------------------------------------

""" DialogError

------------------------------------------------------------------------

	Descripcion:
	Dialogo que se lanza en las siguientes circunstancias:
	
	-No hay ninguna pelicula en la lista: No movies yet
	
	-No hay ninguna pelicula seleccionada: Please, select a movie
	
	-Anadir una pelicula que ya existe: This movie already exists
	
	-Editar una pelicula cambiando sus valores a los de otra que ya
	existe: This movie already exists
	
	-Obtener recomendaciones sin tener ninguna pelicula vista: No
	watched movies yet
	
	-Error al conectarse al servicio en red: An error ocurred: Cannot connect 
	with themoviedb. Make sure you have requests installed
	
	-No se encuentran recomendaciones: Sorry, no recommendations found
	
	-Error al buscar recomendaciones: An error ocurred while looking for
	recommendations. Make sure your key is correct
	
	-Anadir, editar o borrar cuando el filtro muestra las peliculas
	recomendadas: You can't change the recommendations list!
	
	-Pulsar Add, Edit o Delete cuando hay una ventana de entrada de texto
	abierta: You have another window opened. Close it first, please
	
"""
class DialogError(Gtk.Dialog):

    def __init__(self, parent, dialogtext):
        
        Gtk.Dialog.__init__(self, _("ERROR"), parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)
		
        label = Gtk.Label(dialogtext)

        box = self.get_content_area()
        box.add(label)
        self.show_all()



""" DialogWarning
	
------------------------------------------------------------------------
	
	Descripcion:
	Dialogo que se lanza en las siguientes circunstancias:
	
	-Borrar una pelicula: This movie will be deleted. Are you sure?

"""
class DialogWarning(Gtk.Dialog):
	
	def __init__(self, parent, dialogtext):
		
		Gtk.Dialog.__init__(self, _("WARNING"), parent, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
		
		self.set_default_size(150, 100)
		
		label = Gtk.Label(dialogtext)
		
		box = self.get_content_area()
		box.add(label)
		self.show_all()



#-----------------------------------------------------------------------

""" MovieController

------------------------------------------------------------------------
	
	Descripcion:
	Controlador de la aplicacion.
	Inicia el modelo y la vista de la ventana principal.
	Controla las acciones de todos los botones.
	Controla el filtro de peliculas.
	Controla el menu desplegable.
	Controla la generacion de recomendaciones de peliculas.
	Lanza los dialogos.
	
------------------------------------------------------------------------

	Atributos:
	
	self.entry_window_opened: True si hay una ventana de entrada
	de texto abierta, False en caso contrario
	
	self.model: Modelo de la ventana principal
	
	self.view: Vista de la ventana principal

	self.button_recv: Nombre del boton pulsado
	
	self.moviesIDList: Lista de IDs de peliculas
	
	self.language: Idioma
	
	self.entrymodel: Modelo de la ventana de entrada de texto
	
	self.entryview: Vista de la ventana de entrada de texto
	
------------------------------------------------------------------------

	Metodos:
	
	__init__: Inicializacion
	
	--------------------------------------------------------------------
	
	Metodos de control:
	
	on_selection_button_clicked: Funcionamiento de los botones
	
	watched_filter_func: Funcionamiento del filtro
	
	on_show_combo_changed: Funcionamiento del menu desplegable
	
	recommendations_func: Funcionamiento del generador de recomendaciones
	
	--------------------------------------------------------------------
	
	Metodos de lanzamiento de dialogos:
	
	launch_error_dialog: Lanza un dialogo de error
	
	launch_warning_dialog: Lanza un dialogo de aviso
	
	--------------------------------------------------------------------
	
	Metodos que devuelven informacion:
	
	tree_selection_info: devuelve un treemodel y un iterador
	
	movie_info: devuelve el nombre una pelicula y su estado
	
	secondary_movie_info: devuelve el contenido de la entrada de texto
	y el checkbutton (nombre y estado de la nueva pelicula)
	
	--------------------------------------------------------------------
	
	Metodos basicos:
	
	main_add_movie: lanza una ventana para anadir una pelicula
	
	add_movie: anade una pelicula a la lista de peliculas
	
	delete_movie: elimina una pelicula de la lista de peliculas
	
	main_edit_movie: lanza una ventana para editar una pelicula
	
	edit_movie: sustituye la pelicula seleccionada por la nueva
	
	main_add_recommendations: solicita recomendaciones a themoviedb
	
	add_recommendations: anade las recomendaciones a la lista de peliculas
	
	add_movieID: anade el id de una pelicula a la lista de ids
	
	--------------------------------------------------------------------
	
	Otros metodos:
	
	secondary_window_action: controla la ventana de entrada de texto
	
	single_row_action: controla las acciones sobre una pelicula seleccionada
	
	scroll_through_list: recorre la lista de peliculas con diversos objetivos
	
	unicodemovies: devuelve el nombre de una pelicula sin tildes
	
	setfalse: Pone entry_window_opened a Falso
	
"""
class MovieController():
	
	
	def __init__(self):
		self.entry_window_opened = False
		self.model = MovieModel(self)
		self.view = MovieView(self)
		self.view.connect("delete_event", Gtk.main_quit)
		self.view.show_all()


	
	
	def on_selection_button_clicked(self, button):
		
		self.button_recv = button.get_label()
		
		if (self.button_recv == _("Add")) or (self.button_recv == _("Edit")) or \
		(self.button_recv == _("Delete")):
			
			if self.entry_window_opened:
				self.launch_error_dialog(_("You have another window opened. Close it first, please"))
			
			else:
			
				if self.view.current_filter_watched == "r":
					self.launch_error_dialog(_("You can't change the recommendations list!"))
				
				else:		
					if self.button_recv == _("Add"):
						self.main_add_movie()
					else:
						self.single_row_action()
			
		elif (self.button_recv == _("Add ")) or (self.button_recv == _("Edit ")):
			self.secondary_window_action()
			
		elif self.button_recv == _("Cancel"):
			self.entryview.destroy()
			self.entry_window_opened = False
			
	
	
	
	def watched_filter_func(self, model, iter, data):
		
		if self.view.current_filter_watched is None or \
		self.view.current_filter_watched == "None":
			return True
		
		else:
			return model[iter][1] == self.view.current_filter_watched
	
	
	
	
	def on_show_combo_changed(self, combo):
	
		self.scroll_through_list(None, None,"delete")
	
		tree_iter = combo.get_active_iter()
	
		if tree_iter != None:
	
			combo_recv = combo.get_model()
	
			if combo_recv[tree_iter][0]	== _("Show all movies"):
				self.view.current_filter_watched = None
	
			elif combo_recv[tree_iter][0] == _("Show watched movies"):
				self.view.current_filter_watched = "w"
	
			elif combo_recv[tree_iter][0] == _("Show unwatched movies"):	
				self.view.current_filter_watched = "u"
	
			elif combo_recv[tree_iter][0] == _("Show recommendations"):
				self.recommendations_func()
				self.view.current_filter_watched = "r"
	
			self.view.watched_filter.refilter()	
			
			
			
	
	def recommendations_func(self):		
		
		self.moviesIDList = list()
		(self.language,x) = locale.getdefaultlocale()
		
		if (len(self.model.moviesList) == 0) or \
		not (self.scroll_through_list(None,"w","findbyw")):
			self.launch_error_dialog(_("No watched movies yet"))

		else:
			
			try:
				moviedbrequest = requests.get("https://api.themoviedb.org/3/movie/?api_key=%s" %KEY)
			
				try:
					self.scroll_through_list(None, None,"moviesID")
					self.main_add_recommendations()
				
					if not (self.scroll_through_list(None, "r", "findbyw")):
						self.launch_error_dialog(_("Sorry, no recommendations found"))
			
				except:
					self.launch_error_dialog(_("An error ocurred while looking for recommendations. Make sure your key is correct"))
			
			except:
				self.launch_error_dialog(_("An error ocurred: Cannot connect with themoviedb. Make sure you have requests installed"))
			
				
					
				
	def launch_error_dialog(self, message):
		
		dialog = DialogError(self.view, message)
		dialog.run()
		dialog.destroy()
			
			
			
			
	def launch_warning_dialog(self, message):
		
		dialog = DialogWarning(self.view, message)
		response = dialog.run()
		dialog.destroy()
		return response				
				
				
				
				
	def tree_selection_info(self):		
		
		treeselection = self.view.treeview.get_selection()
		treeselection.set_mode(Gtk.SelectionMode.SINGLE)
		(aux, iter) = treeselection.get_selected()	
		
		return (aux,iter)	
		
		
			
			
	def movie_info(self, current_list, iter):
		
		movie = current_list.get_value(iter,0)
		watched = current_list.get_value(iter,1)
		
		return (movie,watched)
		
		
			
			
	def secondary_movie_info(self):
	
		movie = self.entrymodel.entry.get_text()
		
		if self.entrymodel.checkwatched.get_active():
			watched = "w"
		else:
			watched = "u"		
		
		return (movie,watched)			
							
				
				
				
	def main_add_movie(self):

		self.entry_window_opened = True
		self.entrymodel = EntryModel(self)
		self.entryview = EntryView(self)
		self.entryview.connect("delete_event", self.setfalse)
	
	
	
	
	def add_movie(self, movie, watched):

		self.model.moviesList.append([movie,watched])	
	
	
	
	
	def delete_movie(self):

		self.model.moviesList.remove(self.view.iter)
	
	
			
	
	def main_edit_movie(self):

		self.entry_window_opened = True
		self.entrymodel = EntryModel(self)
		self.entryview = EntryView(self)




	def edit_movie(self, movie, watched, iter):

		self.view.iter = iter
		self.model.moviesList.insert_after(self.view.iter,[movie,watched])
		self.model.moviesList.remove(self.view.iter)




	def main_add_recommendations(self):

		for i in self.moviesIDList:
			movie_id = i
			request = requests.get("https://api.themoviedb.org/3/movie/%d/recommendations?api_key=%s&language=%s" %(movie_id,KEY,self.language))
			result = json.loads(request.text)
			self.add_recommendations(result)


	

	def add_recommendations(self, result):
		
		counter = 0
			
		for i in result['results']:
			if counter == 5:
				break
			movie = i['title']
			unicodemovie = self.unicodemovies(movie)
		
			if not (self.scroll_through_list(unicodemovie,None,"findbym")):
				self.model.moviesList.append([unicodemovie,"r"])
				counter = counter+1


		
		
	def add_movieID(self, response):

		for i in response['results']:
			if i['id'] != None:
				self.moviesIDList.append(i['id'])
				break		
		
		
			
		
	def secondary_window_action(self):
		
		(movie,watched) = self.secondary_movie_info()
		iter = self.view.iter
		
		if self.button_recv == _("Add "):
			
			if self.scroll_through_list(movie, None, "findbym"):
				self.launch_error_dialog(_("This movie already exists"))
			
			else:
				self.add_movie(movie, watched)
				self.entryview.destroy()
		
		else:
			
			if self.scroll_through_list(movie, watched, "find") or \
			(movie.lower() != self.entrymodel.oldmovie.lower() and \
			self.scroll_through_list(movie, watched, "findbym")):
				self.launch_error_dialog(_("This movie already exists"))
			
			else:	
				self.edit_movie(movie, watched, iter)
				self.entryview.destroy()
	
		self.entry_window_opened = False
					
	
	
	
	def	single_row_action(self):
		
		if self.view.current_filter_watched == "r":
			self.launch_error_dialog(_("You can't change the recommendations list!"))
		
		else:
		
			if len(self.model.moviesList) == 0:
				self.launch_error_dialog(_("No movies yet"))

			else:
				(aux, iter) = self.tree_selection_info()	
			
				if iter is None:
					self.launch_error_dialog(_("Please, select a movie"))

				else:
					(movie,watched) = self.movie_info(aux, iter)
				
					if self.scroll_through_list(movie, None, "findbym"):
						
						if self.button_recv == _("Delete"):
							response = self.launch_warning_dialog(_("This movie will be deleted. Are you sure?"))
						
							if response == Gtk.ResponseType.OK:
								self.delete_movie()
						
						else:
							self.main_edit_movie()
							

			
			
			
	def scroll_through_list(self, movie, watched, target):
		
		self.view.iter = self.model.moviesList.get_iter_first()
		length = len(self.model.moviesList)
		i = 0
		
		while i < length:
				
			if (target == "find") and (self.model.moviesList.get_value(self.view.iter,0).lower() == movie.lower()) \
			and (self.model.moviesList.get_value(self.view.iter,1) == watched):
				return True
				
			elif (target == "findbym") and (self.model.moviesList.get_value(self.view.iter,0).lower() == movie.lower()):
				return True
					
			elif (target == "findbyw") and (self.model.moviesList.get_value(self.view.iter,1) == watched):
				return True
			
			elif (target == "delete") and (self.model.moviesList.get_value(self.view.iter,1) == "r"):
				self.model.moviesList.remove(self.view.iter)
				
			elif (target == "moviesID") and (self.model.moviesList.get_value(self.view.iter,1) == "w"):
				(movie, watched) = self.movie_info(self.model.moviesList, self.view.iter)
				request = requests.get("https://api.themoviedb.org/3/search/movie/?api_key=%s&language=%s&query=%s" %(KEY, self.language, movie))
				response = json.loads(request.text)
				self.add_movieID(response)
				self.view.iter = self.model.moviesList.iter_next(self.view.iter)

			else:
				self.view.iter = self.model.moviesList.iter_next(self.view.iter)
		
			i = i+1
		
		return False

			
	
	
	def unicodemovies(self, movie):
		result = ''.join((c for c in unicodedata.normalize('NFD',unicode(movie)) if unicodedata.category(c) != 'Mn'))
		return result.decode()

	def setfalse(self, arg1, arg2):
		self.entry_window_opened = False
			
#-----------------------------------------------------------------------

c = MovieController()
Gtk.main()
