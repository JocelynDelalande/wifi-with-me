%rebase base page='map'

<!-- <span class="back-link">&larr; <a href="/">Accueil</a></span> -->

<h1>Résultats</h1>

<div id="map" class="results" data-json="{{geojson}}"></div>
<script src="assets/map.js" type="text/javascript"></script>
<p>Légende : <br />
  <img src="assets/leaflet/images/marker-icon-red.png" /> Personne souhaitant partager sa connexion Internet<br />
  <img src="assets/leaflet/images/marker-icon.png" /> Personne souhaitant se connecter au réseau radio
</p>
<p>
  Télécharger le fichier <a href="{{geojson}}">GeoJSON</a> (base de données mise sous
  licence <a href="http://opendatacommons.org/licenses/by/summary/">ODC-BY
  1.0</a>).
</p>
