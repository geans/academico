import os
from PyGameLearningEnvironment.ple.games import  Pong
from PyGameLearningEnvironment.ple import PLE
from cmac_agent import CmacAgent

def get_ver_distance(state):
    return abs(int(state['ball_y']) - int(state['player_y']))

show_game = True

if not show_game:
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.environ["SDL_VIDEODRIVER"] = "dummy"

game = Pong()

p1 = PLE(game, fps=30, display_screen=not show_game, force_fps=show_game)
p2 = PLE(game, fps=30, display_screen=show_game, force_fps=not show_game)
myAgent = CmacAgent(p1.getActionSet())
for p in [p1, p2]:
    p.init()

    print('Actions:',p.getActionSet())

    nb_frames = 60*5
    k = 1
    old_score = 0
    score = 0

    for f in range(100):
        print('Episode {}'.format(k))
        k += 1
        total_reward = 0
        total_cust_reward = 0
        for f in range(nb_frames):
            if p.game_over(): #check if the game is over
                p.reset_game()

            # get current state
            state = game.getGameState()
            previus_distance = get_ver_distance(state)
            # pick action based on q_function and current state
            action = myAgent.pick_action(state)
            # apply action and get reward
            reward = p.act(action)
            total_reward += reward
            score = game.getScore()
            if score != old_score and score > 0:
                print('Score {}'.format(game.getScore()))
                pass
            old_score = score
            # get next state
            next_state = game.getGameState()
            new_distance = get_ver_distance(next_state)

            customize_reward = -5
            if new_distance == 0:  # agent will rebut the ball
                customize_reward = 10
            elif new_distance < previus_distance:
                customize_reward = 5
            elif new_distance > previus_distance:
                customize_reward = -20
            # if reward > 0:
            #     customize_reward += reward * 10
            total_cust_reward += customize_reward

            # update q_function with state, next_state, action and reward
            myAgent.update_q_function(state, action, customize_reward, next_state)
        print(total_reward, total_cust_reward)
        p.reset_game()
