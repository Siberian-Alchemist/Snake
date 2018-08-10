import colors

window_width = 500
window_height = 500
background_image = 'images/background.png'
snake_head_image = 'images/snake_head.png'
snake_tail1_image = 'images/snake_tail_1.png'
snake_tail2_image = 'images/snake_tail_2.png'
apple_image = 'images/apple.png'

frame_rate = 6

start_pos_x = 250
start_pos_y = 250
head_w = 30
head_h = 30
tail_w = 30
start_length = 2
speed = [0, -30]
text_color = colors.BLACK
apple_radius = 30

font_name = 'Arial'
font_size = 25

sounds_effects = dict(
    eaten='sounds/eaten.ogg',
    game_over='sounds/game_over.ogg'
    )

message_duration = 2
score_offset = 5
status_offset_y = 5

