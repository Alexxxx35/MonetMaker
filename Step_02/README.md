Nous avons intégré deux paramètres supplémentaires dans la ligne de commande du programme pour séléctionner le type de floutage à appliquer: linéaire,médian ou gaussian.

```
cli.add_argument("-b", "--blur", type=blur, choices=list(blur), required=False,
                 help="Blur method pre-applied before Canny Edge Detection (linear, gaussian or radial)")
```

L'unité de mesure du floutage, qui détermine son intensité, aussi appelé kernel est le second paramètre de la ligne de commande que nous implémentons sur cette étape:
```
cli.add_argument("-k", "--kernel", required=False,
                 help="kernel level of blurring")

```
Le kernel est un masque qui modifie la valeur des pixels sur la base de la valeur des pixels alentours. Les pixels autour du pixel central sont appelés les "pixels voisins". Lorsque le masque se déplace sur l'image pixel par pixel, la valeur du pixel central est ainsi modifiée en fonction de la valeur des pixels voisins. (voir image kernel.png) Comme on peut le voir sur l'image la taille du masque est determinée par les valeurs du kernel en ligne de commande. Plus le kernel est grand, plus le pixel central a de pixels voisins pris en compte lors du calcul et inversement ce qui impacte le résultat final.

L'image est floutée en fonction du choix effectué en ligne de commande, son information (matrices de pixels) est stockée dans la variable blurred pour le reste du traitement de détection des bords et est affichée à l'écran:
```
cv.imshow("Canny Edge Detection", blurred)
```

Par défaut, l'algorithme Canny applique un floutage gaussian à l'image d'entrée dans l'objectif d'en réduire le bruit.

En fin de compte, quel que soit le flou employé, le résultat est relativement similaire sur les images que nous avons utilisées. En revanche, nous avons estimé qu'un kernel de 3 était le plus fiable pour le calcul de contours de bords.