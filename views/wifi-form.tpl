%rebase base page='form'
  <script src="assets/form.js" type="text/javascript"></script>

  <header class="jumbotron">
    <div class="container">
%if errors:

<p>
  Veuillez corriger les <span class="label label-danger">erreurs</span>
  suivantes :
</p>
<div id="errors" class="bg-danger">
<ul >
%for field, err in set(errors):
  <li><strong>{{field}}</strong> : {{err}}</li>
%end
</ul>
</div>

%else:
    <p>
L'association <a href="http://www.illyse.net">Illyse</a> expérimente à
grande échelle (Lyon, Monts du Lyonnais et alentours) la création d'un réseau sans-fil à
longue portée pour permettre, entre autres, le <em>partage</em> et
la <em>fourniture</em> d'<strong>accès à Internet</strong>.
    </p>

    <p>
Pour cela, nous recherchons des volontaires intéressés pour participer au projet,
que ce soit pour <strong>obtenir un accès à Internet Illyse</strong> via ce réseau radio,
pour <strong>partager une partie de leur connexion existante</strong>
ou pour <strong>propager le réseau radio</strong> en relayant le signal.
    </p>

      <p>
Renseigner ce formulaire nous permet de définir <strong>quelles zones
couvrir en priorité</strong> pour lancer le projet.
      </p>
%end
    </div>
  </header>

  <section role="main" class="container">
  <form role="form" method="post">

    <h2>Contact</h2>
    <div class="form-group">
    <label for="name">Nom / Pseudo</label>
    <input name="name" value="{{data.get('name', '')}}"
           id="name" type="text" class="form-control"/>
    </div>

    <div class="row">
      <div class="form-group col-md-6">
        <label for="email">Email</label>
        <input name="email" value="{{data.get('email', '')}}"
               id="email" type="email" class="form-control">
        <p class="help-block">
          <span class="glyphicon glyphicon-warning-sign"></span>
          Un moyen de contact au moins est nécessaire
        </p>
      </div>
      <div class="form-group col-md-6">
        <label for="phone">Téléphone</label>
        <input name="phone" value="{{data.get('phone', '')}}"
               id="phone" type="tel" class="form-control"/>
      </div>
    </div>

    <h2>Je souhaite</h2>
    <p class="radio">
      <label>
      <input type="radio" name="contrib-type" value="share"
             {{'checked' if data.get('contrib-type') == 'share' else ''}}/>
      Partager une partie de ma connexion Internet existante
      </label>
    </p>
    <p class="radio">
      <label>
      <input type="radio" name="contrib-type" value="connect"
             {{'checked' if data.get('contrib-type') == 'connect' else ''}}/>
      Me raccorder au réseau radio pour bénéficier d'un accès à Internet
      </label>
    </p>

    <div id="contrib-type-share">
    <h2>Partager une connexion</h2>
    <h3>Type de connexion</h3>
    <p class="radio"><label>
      <input {{'checked' if data.get('access-type') == 'fiber' else ''}}
         type="radio" name="access-type" value="fiber"/>
      Fibre
    </label></p>
    <p class="radio"><label>
      <input {{'checked' if data.get('access-type') == 'vdsl' else ''}}
      type="radio" name="access-type" value="vdsl"/>
      VDSL
    </label></p>
    <p class="radio"><label>
      <input {{'checked' if data.get('access-type') == 'adsl' else ''}}
             type="radio" name="access-type" value="adsl"/>
      ADSL
    </label></p>
    <p class="radio"><label>
      <input {{'checked' if data.get('access-type') == 'cable' else ''}}
             type="radio" name="access-type" value="cable"/>
      Câble
    </label></p>

    <div class="form-group">
    <label for="isp">Votre fournisseur d'accès à Internet</label>
    <input name="isp" value="{{data.get('isp', '')}}"
           id="isp" type="text" class="form-control"/>
    </div>

    <h3>Débits</h3>
    <p class="help-block">
      Il est possible de limiter techniquement la quantité de bande passante
    partagée avec les autres expérimentateurs afin de ne pas pénaliser votre
    confort.
    </p>
    <p>
      <label for="bandwidth">Débit total (Mbps)</label>
      <input name="bandwidth" value="{{data.get('bandwidth', '')}}"
             id="bandwidth" type="number" min="0" class="form-control"/>
    </p>
    <p>
      <label for="share-part">Je souhaite partager (au max.) (Mbps)</label>
      <input name="share-part" value="{{data.get('share-part', '')}}"
             id="share-part" type="number" min="0" class="form-control"/>
    </p>
    </div>

    <h2>Ma localisation</h2>

    <div class="row">
      <div class="col-sm-6">
        <div id="map" data-json="{{geojson}}"></div>
      </div>
      <div class="form-group col-sm-6">
        <div class="form-group form-group-lg form-inline">
          <input type="text" name="search"
                 id="search" placeholder="rue de gerland, lyon" class="form-control" />
          <span id="search-btn" class="btn btn-default btn-lg" data-loading-text="...">Recherche</span>

          <div id="search-results" class=""></div>
          <p class="help-block">Déplacer le marqueur bleu pour pointer précisément le bâtiment au besoin</p>
          <p class="help-block">
            Les ronds verts sont ceux renseignés par d'autres utilisateurs, vous
            pouvez aussi consulter <a href="map" target="_blank">la carte
            publique plus détaillée</a>.
          </p>

        </div>
        <input name="latitude" value="{{data.get('latitude', '')}}"
               type="hidden" id="latitude" />
        <input name="longitude" value="{{data.get('longitude', '')}}"
               type="hidden"  id="longitude" />
        </div>
      </div>
    </div>

    <p class="help-block">Les antennes peuvent être positionées soit sur le toit soit aux fenêtres/balcons/velux.</p>

    <div class="form-group">
    <label for="orientation" />Orientation(s) de mes fenêtres, balcons ou velux</label>
    (<label class="checkbox-inline"><input type="checkbox" name="orientation-all" id="orientation-all" value="" />Vue à 360°</label>)
    <br>
%for val, label in orientations:
    <label class="checkbox-inline">
      <input type="checkbox" class="orientation" name="orientation" value="{{val}}"
             {{'checked' if val in data.getall('orientation') else ''}}/>
      {{label}}
    </label>
%end
    </div>

    <div class="form-group">
        <label for="roof">Je peux accéder à mon toit
          <input name="roof" {{'checked' if data.get('roof', False) else ''}}
                 type="checkbox"/>
        </label>
    </div>

    <p class="form-inline">
      <label for="floor">Mon étage</label>
      <input name="floor" value="{{data.get('floor', '')}}"
             id="floor" type="number" class="form-control" placeholder="« 0 » pour le  RDC"/>
      <span>/</span>
      <input name="floor_total" value="{{data.get('floor_total', '')}}"
             id="floor_total" type="number" class="form-control" placeholder="Nb. d'étages du bâtiment"/>
    </p>

    <h2>Remarque/commentaire</h2>
    <textarea name="comment" class="form-control" row="5">{{data.get('comment', '').strip()}}</textarea>

    <h2>Mes données</h2>

    <p class="help-block">
Les données collectées dans ce formulaire sont, par défaut, accessibles
seulement aux membres d'Illyse portant ce projet.<br />

Certaines données, précisées ci-dessous, et anonymisées peuvent-être exposées
sur une carte publique.
    </p>

    <div class="form-group">
    <label for="privacy" />
J'autorise qu'apparaissent sur la carte publique :
    </label><br />
    </div>
    <div class="checkbox">
      <label>
        <input type="checkbox" name="privacy" value="coordinates"
        {{'checked' if (('coordinates' in data.getall('privacy')) or not data) else ''}} />
        Mes coordonnées GPS
      </label>
    </div>
    <div class="checkbox">
      <label>
        <input type="checkbox" name="privacy" value="place_details"
        {{'checked' if (('place_details' in data.getall('privacy')) or not data) else ''}}/>

        Mon étage et mes orientations
      </label>
    </div>
    <div class="checkbox">
      <label>
        <input type="checkbox" name="privacy" value="name"
        {{'checked' if 'name' in data.getall('privacy') else ''}}/>
        Mon nom/pseudo
      </label>
    </div>
    <div class="checkbox">
      <label>
        <input type="checkbox" name="privacy" value="comment"
        {{'checked' if 'comment' in data.getall('privacy') else ''}}/>
        Mon commentaire
      </label>
    </div>
    <!-- if you are human, you do not see me: -->
    <div style="display: none">
      <input name="url" value="{{data.get('url', '')}}"
             id="url" class="form-control">
    </div>
    <input type="submit" value="Envoyer" class="btn btn-primary btn-lg"/>
  </form>
  </section>


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
