
// La fonction shadow prend un événement en entrée
function shadow(event) {
	// Récupère la position x et y de la souris dans l'événement
	const x = event.clientX;
	const y = event.clientY;
	// Calcule les valeurs de l'ombre en fonction de la position de la souris
	const shadowX = (window.innerWidth / 2 - x) / 100;
	const shadowY = (window.innerHeight / 2 - y) / 100;
	// Calcule la valeur du flou de l'ombre en fonction de la position de la souris
	const shadowBlur = Math.abs((window.innerWidth / 2 - x) / 40);
	// Calcule l'étalement de l'ombre en fonction de la position de la souris
	const shadowSpread = Math.abs((window.innerHeight / 2 - y) / 120);

	// Crée une chaîne de caractères qui contient toutes les valeurs calculées de l'ombre, ainsi que la couleur
	const shadowValue = `${shadowX}px ${shadowY}px ${shadowBlur}px ${shadowSpread}px rgba(0, 0, 0, 0.05)`;

	// Applique la valeur de l'ombre à la propriété CSS --box-shadow de l'élément root (la racine) du document HTML
	document.documentElement.style.setProperty('--box-shadow', shadowValue);
}

// Ajoute un écouteur d'événements qui appelle la fonction shadow à chaque fois que la souris bouge sur l'écran
document.addEventListener('mousemove', shadow);


$(document).ready(function(){
	$(".parent").on("mouseenter", ".wimg", function(){
		var coverImagePath = $(this).find("img").attr("src"); // Récupère le chemin de l'image de couverture
		$(".wimg img").attr("src", coverImagePath); // Change l'attribut src de l'image
	}).on("mouseleave", ".wimg", function(){
		$(".wimg img").attr("src", "{{ url_for('static', filename='img/def.jpg') }}"); // Réinitialise l'image de couverture à l'image par défaut
	});
});




$(document).ready(function(){
	wimg = $(".img_containers").width();
	console.log(wimg);
	$(".img_containers").css("height",wimg);

	$(window).resize(function(){
		wimg = $(".img_containers").width();
		console.log(wimg);
		$(".img_containers").css("height",wimg);
	})


	$('#gal .img_containers img').click(function(){
		// $(" #gal .img_containers").removeClass("fullImg");
		$(this).parent().toggleClass("fullImg");
	});

})




