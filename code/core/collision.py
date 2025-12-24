def check_collision(player_rect, obstacles):
    if not player_rect:
        return False
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle["rect"]):
            return True
    return False
