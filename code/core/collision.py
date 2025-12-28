def check_collision(player, obstacles):
    if not player.rect:
        return False
    for obstacle in obstacles:
        if player.rect.colliderect(obstacle["rect"]):
            return True
    return False
    return False
