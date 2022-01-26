Dans un premier temps, nous avons conçu la ligne de commande avec la librairie argparse qui permet au script de chercher le chemin de l'image.

La première étape dans le traitement d'une image en vue de détecter ses contours consiste à réduire le "bruit" d'une image c'est-à-dire modifier la valeur des pixels constituant l'image en appliquant à ceux_ci un filtre. Il simplifie donc l'information mathématique de l'image.

Dans un premier temps, nous convertissons l'image en niveaux de gris. Le code RGB contient beaucoup trop d'informations pour que l'image soit traitée par des algorithmes telle quelle. Ces informations ne sont pas utiles pour la détection de bords et seraient susceptibles de ralentir les algorithmes utilisés plus tard. Une fois l'image grisée, les pixels contiennent une valeur simple comprise entre 0 (noir) et 255 (blanc) (voir image grayscale.png) au lieu d'un ensemble de trois valeurs (voir image rgb_image.png).
```
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
```
Si l'on applique directement l'algorithme Canny en paramétrant les valeurs de seuil manuellement, il est possible d'arriver à un résultat satisfaisant, cependant nous risquons d'avoir une image de sortie avec trop de "bruit" ou alors avec trop peu de contours détéctés au risque de ne pas reconnaitre l'image initiale.

Afin d'obtenir une détection de bords satisfaisante quelque soit l'image de départ, nous allons calculer la médiane des niveaux de gris de l'image donc de sa matrice de pixels.
```
computed_median = np.median(gray)
```

A partir de cette médiane, nous utilisons une technique de segmentation de l'image en définissant un seuil élevé et un seuil faible pour l'algorithme Canny. On cherche à determiner quels pixels sont situés au-dessus et en dessous de ces deux seuils.

 ```
lower_treshold = (1.0 - 0.33) * computed_median
upper_treshold = int(min(255, (1.0 + 0.33) * computed_median))
 ```

On applique ensuite l'algorithme de Canny sur l'image en prenant en compte les deux seuils.
```
automatically_edged = ~cv.Canny(img, lower_treshold, upper_treshold)
```
L'opérateur tild inverse la valeur de chaque bit individuel qui constitue l'image ce qui visuellement inverse la couleur de l'image pour obtenir ce qui était demandé. Le résultat est satisfaisant de notre point de vue sur plusieurs images différentes.
Le tableau concaténé d'images démontre le résultat:
```
np.hstack([tight,wide,automatically_edged])
```
A gauche figure l'image traitée par Canny avec des seuils de gris faible,
au centre des seuils de gris élevés et à droite nous avons l'image traitée par Canny traitée avec la médiane des niveaux de gris.