<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>FAIMaison − contribution à l'expérimentation wifi</title>

    <!-- jQuery -->
    <script src="assets/jquery/jquery-1.11.0.min.js" type="text/javascript"></script>

    <!-- Bootstrap -->
    <script src="assets/bootstrap/js/bootstrap.js"></script>
    <link href="assets/bootstrap/css/bootstrap.min.css" rel="stylesheet">

    <!-- Leaflet -->
    <link rel="stylesheet" type="text/css" media="all" href="assets/leaflet/leaflet.css" />
    <script src="assets/leaflet/leaflet.js" type="text/javascript"></script>

    <!-- Custom -->
    <link rel="stylesheet" type="text/css" media="all" href="assets/main.css" />
    <!-- script src="assets/main.js" type="text/javascript"></script -->

  </head>
<body>
  <header class="jumbotron">
    <div class="container">
    <h1>Réseau wifi expérimental</h1>
  </header>

  <section role="main" class="container">
    <span class="back-link">&larr; <a href="/">Accueil</a></span>

    <div id="map" class="results" data-json="{{geojson}}"></div>
    <script src="assets/map.js" type="text/javascript"></script>
    <p>
      Télécharger le fichier <a href="{{geojson}}">GeoJSON</a>.
    </p>
  </section>

  <footer>
    <p>Vos données personnelles sont en lieu sûr.</p>
  </footer>

  <div id="modal" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="Resultats" aria-hidden="true">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Fermer</span></button>
          <h4 class="modal-title" id="myModalLabel">Résultats</h4>
        </div>
        <div class="modal-body">
        </div>
      </div>
    </div>
  </div>

</body>
</html>
