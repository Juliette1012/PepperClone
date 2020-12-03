# PepperClone

Un pepper bouge aléatoirement ou par l’interaction d’un humain. Un second pepper, immobile, réagit aux différentes postures du premier qu’il reconnaît grâce à sa caméra frontale.

## Fonctionnement :

  1. Création d’une dataset d’entraînement et de test :
  
a. En utilisant les méthodes d’opencv, on enregistre des images des différentes
postures à classifier :
- 1001 images pour la position initiale du pepper
- 1001 pour la position bras levée
- 1001 pour la posture buste baissée

b. Dans un dossier différent, on enregistre le même nombre d’images pour la base de test.


  2. Preprocessing des images en vue de l’entraînement d’un réseau de neurones
  
a. Conversion des images RGB en grayscale (la couleur n’est pas utile à la classification).
b. Extraction des features (matrices de pixels) et assignation des labels à chaque posture (0 for standing, 1 for crouching and 2 for raising) en vue de
faire de l’apprentissage supervisé.
c. Reshape de la matrice de pixels en tableau numpy de la taille du nombre de features.
d. Sauvegarde des données sous formes “X_train, y_train” dans des fichiers pickle facilement manipulables.

  3. Entraînement d’un modèle type CNN
  
a. Normalisation
b. OneHotEncoder pour reformater les données en un vecteur de 3 bits
c. Modélisation d’un CNN :
  - Une couche de data augmentation (horizontal et contraste) pour agrandir la taille des données d’entraînement.
  - 3 couches de convolution avec des fonctions d’activation ‘relu’
  - Une couche head avec en sortie 3 neurones pour faire la classification en catégorie avec la fonction d’activation ‘softmax’.
  - On entraîne le modèle avec en fonction de perte `categorical_crossentropy`, l’optimizer `adam` et l’accuracy comme métrique.
  - On définit la batch_size à 32 et on entraîne pendant 30 epochs.
  
  4. Évaluation du modèle avec une base de données test
  5. Utilisation du modèle dans le simulateur qibullet (réaction du pepper en fonction de la prédiction)
 
  6. Test de la prédiction dans un environnement différent (présence d’une table dans l’environnement)


## Pour aller plus loin :

Il aurait été possible à la place d’un CNN d’utiliser une architecture hybride : CNN-LSTM.
Le CNN permettrait d’extraire les features nécessaires et le LSTM permettrait d’analyser, mémoriser la séquence de frames et ainsi permettre de déterminer la posture que le pepper va adopter et ainsi cela permettrait d’être dans une sorte d’anticipation, et donc aller vers de l’optimisation dans la réaction du pepper aux différentes postures du pepper visible.
