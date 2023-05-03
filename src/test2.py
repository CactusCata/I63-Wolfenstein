from math import pi, cos, acos, sin, sqrt

def prod_scalaire_2(u, v):
    return u[0] * v[0] + u[1] * v[1]

def norme_2(vec):
    return sqrt(prod_scalaire_2(vec, vec))

def entity_is_visible(mob_pos, player_pos, player_rot, fov):
    u = (mob_pos[0] - player_pos[0], mob_pos[1] - player_pos[1])
    v = (cos(player_rot), sin(player_rot))
    norme_u = norme_2(u)
    prod_scal_uv = prod_scalaire_2(u, v)
    angle = acos(prod_scal_uv / norme_u)

    return angle * 180 / pi < fov // 2

def get_visibles_entity(mobs_pos, player_pos, player_rot, fov):
    visibles_entities = []
    for mob_pos in mobs_pos:
        if entity_is_visible(mob_pos, player_pos, player_rot, fov):
            visibles_entities.append(mob_pos)
    return visibles_entities


if __name__ == "__main__":
    mobs_pos = [(0.5, 1), (3, 4), (1, 3), (1.5, 1), (4, 2.5)]
    player_pos = (2.5, 3)
    player_rot = 0 * pi / 180
    fov = 60

    print(get_visibles_entity(mobs_pos, player_pos, player_rot, fov))

"""
algo du peintre: on dessine tout puis on dessine le sprite d'alien
si on ne bouge pas et que l'alien bouge, on lift le dessin de mur et on redessine l'alien
si on bouge, on recalcul tout
"""