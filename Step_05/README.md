Pour cette étape nous allons employer une méthode de classification des pixels en différents groupes. Une fois ces groupes établis, l'agent sera de déterminer les couleurs appropriées à utiliser pour colorer l'image qu'il dessine.

Nous lui donnons donc une palette de couleurs en amont avec les valeurs rgb.

```
COLOR_PALETTE = {0: (112, 78, 46), 1: (121, 116, 46),
                 2: (194, 231, 127), 3: (230, 248, 178),
                 4: (112, 145, 118)}
```

Nous utilisons une première fonction "pixel_closest_color_from_palette" qui va parcourir la palette de couleurs au moment ou nous parcourons la matrice de pixels de l'image. Pour chaque pixel, la fonction va calculer la distance de couleur entra chaque valeur rgb de l'image et l'additionner:

```
for i, rgb_value in enumerate(pixel_rgb):
    result += abs(rgb_value-rgb_tuple[i])
distances.append(result)
```
Cette fonction est donc incluse dans une autre fonction "classify_pixels" qui parcourt la matrice de pixels de l'image initiale afin d'itérer sur chaque valeur rgb de chaque pixel. Cette dernière fonction va au cours de l'itération remplacer la valeur rgb de chaque pixel par celle de la palette la plus proche de la valeur initiale rgb du pixel.
```

for i, rgb in enumerate(pixel_row):
            pixel_row[i] = pixel_closest_color_from_palette(
                rgb, color_palette)
    return matrix
```
La nouvelle matrice est ensuite retournée.
Le module tqdm mesure la durée d'exécution de cette opération puisqu'il ne se passe rien graphiquement.

La fonction "draw" récupère la nouvelle matrice en paramètre et dessine la nouvelle matrice de pixels en utilisant les coordonnées des axes de turtle.
Il nous faut au préalable définir la portée des couleurs pour le pinceau de turtle afin que le changement de couleurs soit fonctionnel par la suite:
```
screen.colormode(255)
```
Ensuite nous refaisons la simulation d'impression en levant le pinceau lorsque le curseur revient au début de chaque rangée de pixels et nous le posons pour commencer le dessin. A chaque pixel parcouru sur la nouvelle matrice, nous changeons la couleur du pinceau avant de dessiner. 
Nous faisons une update de l'écran à chaque rangée de pixels parcouru pour conserver l'effet d'impression au sein de la fonction.

```
for y in range(int(image_height/2), int(image_height/-2),  -1):
    pen.penup()
    pen.goto(-(image_width / 2), y)
    pen.pendown()
    for x in range(-int(image_width/2), int(image_width/2), 1):
        pix_width = int(x + (image_width/2))
        pix_height = int(image_height/2 - y)
        pen.color(new_matrix[pix_height, pix_width])
        pen.forward(1)
    screen.update()
```
