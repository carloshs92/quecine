$(document).ready(function(){
	//VARIABLES
	var URL = "http://quecine.herokuapp.com/"

	var CINE = new Object();
	CINE.CINEPLANET = 0;
	
	var urlCines = URL + "cines/?format=json"
	var urlPeliculas = URL + "peliculas/?format=json"
	var urlHorarios = URL + "horarios/?format=json"
	
	var quecine = {};
	window.indexedDB = window.indexedDB || window.webkitIndexedDB || window.mozIndexedDB;

	if ('webkitIndexedDB' in window) {
	  window.IDBTransaction = window.webkitIDBTransaction;
	  window.IDBKeyRange = window.webkitIDBKeyRange;
	}

	quecine.indexedDB = {};
	quecine.indexedDB.db = null;

	quecine.indexedDB.onerror = function(e) {
  		console.log(e);
	};

	quecine.indexedDB.open = function() {
		var version = 1;
		var request = indexedDB.open('quecine', version);

		request.onupgradeneeded = function(e) {
		    var db = e.target.result;
		    e.target.transaction.onerror = quecine.indexedDB.onerror;

		    if(db.objectStoreNames.contains("cines")) {
		    	db.deleteObjectStore("cines");
		    }

		    if(db.objectStoreNames.contains("peliculas")) {
		    	db.deleteObjectStore("peliculas");
		    }

		    if(db.objectStoreNames.contains("horarios")) {
		    	db.deleteObjectStore("horarios");
		    }

		    var storeCines = db.createObjectStore("cines", {keyPath: "cod"});
		    var storePeliculas = db.createObjectStore("peliculas", {keyPath: "cod"});
		    var storeHorarios = db.createObjectStore("horarios", {keyPath: "cod"});

		    cargarCines();
				cargarPeliculas();
				cargarHorarios();
		};

		request.onsuccess = function(e){
			quecine.indexedDB.db = e.target.result;
			console.log('Se creo la base de datos')
		}
	};

	quecine.indexedDB.addCinema = function(cod, cine, lat, lon, direccion, sede) {
		var db = quecine.indexedDB.db;
		var trans = db.transaction(["cines"], "readwrite");
		var store = trans.objectStore("cines");
		var request = store.put({
	    	"cod": cod,
	   		"cine": cine,
	   		"lat": lat,
	   		"lon" : lon,
	   		"direccion": direccion,
	   		"sede" : sede
	  	});

	    request.onsuccess = function(e) {
	  		console.log('Se guardo el cine exitosamente');
	  	};

	  	request.onerror = function(e) {
	    	console.log('exploto D:');
	  	};
	};

	quecine.indexedDB.addMovie = function(cod, pelicula, trailer) {
		var db = quecine.indexedDB.db;
		var trans = db.transaction(["peliculas"], "readwrite");
		var store = trans.objectStore("peliculas");
		var request = store.put({
	    	"cod": cod,
	   		"pelicula": pelicula,
	   		"trailer": trailer
	  	});

	    request.onsuccess = function(e) {
	  		console.log('Se guardo la pelicula exitosamente');
	  	};

	  	request.onerror = function(e) {
	    	console.log(e.value);
	  	};
	};
	
	// var request = store.get(id); 
	quecine.indexedDB.addSchedule = function(cod, pelicula, cine, tipo, horarios) {
		var db = quecine.indexedDB.db;
		var trans = db.transaction(["horarios"], "readwrite");
		var store = trans.objectStore("horarios");
		var request = store.put({
	    	"cod": cod,
	   		"pelicula": pelicula,
	   		"cine": cine,
	   		"tipo": tipo,
	   		"horarios" : horarios
	  	});

	    request.onsuccess = function(e) {
	  		console.log('Se guardo el horario exitosamente');
	  	};

	  	request.onerror = function(e) {
	    	console.log(e.value);
	  	};
	};

	function cargarCines(){
		$.ajax({
			dataType: "json",
			url: urlCines,
			success: function(data){
				$.each(data, function(key, val){
					console.log(val.cine)
					quecine.indexedDB.addCinema(val.cod, val.cine, 0, 0, "-", val.sede.split('/')[4]);
				});
			}
		});
	}

	function cargarPeliculas(){
		$.ajax({
			dataType: "json",
			url: urlPeliculas,
			success: function(data){
				$.each(data, function(key, val){
					console.log(val.pelicula)
					quecine.indexedDB.addMovie(val.cod, val.pelicula, "http://www.youtube.com/watch?v=EJ-bYOyQ46Y");
				});
			}
		});
	}

	function cargarHorarios(){
		$.ajax({
			dataType: "json",
			url: urlHorarios,
			success: function(data){
				$.each(data, function(key, val){
					console.log(val.id)
					quecine.indexedDB.addSchedule(val.id, val.pelicula.split('/')[4], val.cine.split('/')[4], val.tipo, val.horarios);
				});
			}
		});
	}

	function getVideoID(trailer){
		return trailer.split('=')[1]
	}

	function listarPeliculas(){
		var db = quecine.indexedDB.db;
		var trans = db.transaction(["peliculas"], "readwrite");
		var store = trans.objectStore("peliculas");

		var cursorRequest = store.openCursor();

  	$('#result').html('<ul id="peliculas"></ul>');
	  html = '<ul>';
	  cursorRequest.onsuccess = function(e) {
	    var result = e.target.result;
	    if(!!result == false)
	      return;
	    renderMovies(result.value)
	    //img = '<aside class="pack-end"><img alt="trailer" style="height:auto;margin-top: 7px;" src="http://img.youtube.com/vi/'+getVideoID(result.value.trailer)+'/2.jpg"></aside>'
	    //html += '<li>'+img+'<a href="#" data-id="'+result.value.cod+'"><p>'+result.value.pelicula+'</p></a></li>';
	    result.continue();
	    //html += '</ul>';
		  //$('#result').html(html);
	  };
	}

	function obtenerPelicula(id){
		var db = quecine.indexedDB.db;
		var trans = db.transaction(["peliculas"], "readwrite");
		var store = trans.objectStore("peliculas");
		var request = store.get(id); 
		request.onsuccess = function(e){
			 var result = e.target.result;
			 console.log(result.pelicula)
		}
	}

	function renderMovies(row){
		var ul = document.getElementById("peliculas");
		var aside = document.createElement("aside");
		var img = document.createElement("img");
		var li = document.createElement("li");
		var a = document.createElement("a");
		var p = document.createElement("p");

		aside["class"] = "pack-end";
		img["alt"] = "trailer";
		img["style"] = "height:auto;margin-top: 7px;";
		img["src"] = "http://img.youtube.com/vi/"+getVideoID(row.trailer)+"/2.jpg";
		a["href"] = "#";
		a["data-id"] = row.cod;
		p["textContent"] = row.pelicula;

		a.addEventListener("click", function() {
    	obtenerPelicula(row.cod);
  	}, false);

		aside.appendChild(img);
		a.appendChild(p);
		li.appendChild(aside);
		li.appendChild(a);
		ul.appendChild(li);

	}


	
	$('.list-movies').click(function(){
		listarPeliculas();
	});

	function init() {
	  quecine.indexedDB.open();
	}

	window.addEventListener("DOMContentLoaded", init, false);
});