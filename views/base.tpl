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
    <!-- Leaflet-semicircle -->
    <script src="assets/leaflet-semicircle/semicircle.js" type="text/javascript"></script>

    <!-- Custom -->
    <link rel="stylesheet" type="text/css" media="all" href="assets/main.css" />


  </head>
<body class="{{page}}">

  <header class="main-header jumbotron">
    <div class="container">
    %if page == 'form':
    <h1>Réseau wifi expérimental</h1>
    %else:
    <h1><a href="./">Réseau wifi expérimental</a></h1>
    %end
    </div>
  </header>

  <section role="main" class="container">
  %include
  </section>

  <footer>
    <p>
        Vos données personnelles sont en lieu sûr.
        <br>
        <a href="https://www.faimaison.net" target="_blank">FAImaison.net</a> -
        <a href="./legal">Mentions légales</a>
    </p>
  </footer>

</body>
</html>
