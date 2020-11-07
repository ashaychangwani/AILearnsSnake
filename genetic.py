import random
import pickle
import time
from boundary import Playground
import snake

width = 540
height = 440
block_size = 10
layers = [24, 16, 3]
random_params = True
population_size = 50
no_of_generations = 45
per_of_best_old_pop = 30.0  # percent of best performing parents to be included
per_of_worst_old_pop = 2.0  # percent of worst performing parents to be included
mutation_percent = 7.0
mutation_intensity = 0.1


def progress_bar(curr, total, length):
    frac = curr/total
    filled_bar = round(frac*length)
    print('\r', '#'*filled_bar + '-'*(length - filled_bar),
          '[{:>7.2%}]'.format(frac), end='')


def run(snakes, playground):
    i = 1
    count = [0 for _ in range(300)]
    snakes_killed = 0

    env_seed = random.random()
    for snake in snakes:
        start_time = time.time()
        checkloop = False
        progress_bar(i, population_size, 30)
        random.seed(env_seed)
        snake.neuralnet.setNextFood(
            playground.create_new_apple(snake.snake_position))
        while(snake.isAlive()):
            result = snake.neuralnet.decision(
                snake.head_x, snake.head_y, snake.snake_position, snake.direction)

            if snake.steps_taken > 250:
                if not checkloop:
                    checkloop = True
                    any_point_of_loop = (snake.head_x, snake.head_y)
                    times = 0
                elif (snake.head_x, snake.head_y) == any_point_of_loop:
                    times += 1
                if times > 2:
                    snake.collision_with_boundary = True
                    snake.collision_with_self = True
                    snakes_killed += 1
            else:
                checkloop = False
            if time.time() - start_time > 0.5:
                snake.collision_with_boundary = True
                snake.collision_with_self = True
                snakes_killed += 1
            if (snake.head_x, snake.head_y) == playground.food:
                snake.steps_taken = 0
                result = snake.neuralnet.decision(
                    snake.head_x, snake.head_y, snake.snake_position, snake.direction)
                if not snake.updateSnakePosition(result):
                    snake.collision_with_boundary = True
                start_time = time.time()
                snake.neuralnet.setNextFood(
                    playground.create_new_apple(snake.snake_position))
            if snake.move(result) == False:
                break
        random.seed()
        count[len(snake.snake_position) - 1] += 1
        i += 1

    print('\nsnakes distribution with index as score : ',
          count[0:15], 'snakes killed', snakes_killed)


def print_top_5(five_snakes):
    i = 0
    for snake in five_snakes:
        i += 1
        print('snake : ', i, ', score : ', len(snake.snake_position) -
              1, ', steps : ', snake.steps_taken, end='\t')
        if snake.collision_with_self and snake.collision_with_boundary:
            print('crashed repetition')
        elif snake.collision_with_boundary and not snake.collision_with_self:
            print('crashed wall')
        else:
            print('crashed body')


def save_top_snakes(snakes, filename):
    f = open(filename, "wb")
    pickle.dump(snakes, f)
    f.close()


def create_new_pop(snakes):
    parents = []
    top_old_parents = int(population_size * per_of_best_old_pop / 100)
    bottom_old_parents = int(population_size * per_of_worst_old_pop / 100)

    for i in range(top_old_parents):
        parent = snake.snake(width, height, layers, block_size, False)
        parent.neuralnet.weights = snakes[i].neuralnet.weights
        parent.neuralnet.bias = snakes[i].neuralnet.bias
        parents.append(parent)

    for i in range(population_size - 1, population_size - bottom_old_parents-1, -1):
        parent = snake.snake(width, height, layers, block_size, False)
        parent.neuralnet.weights = snakes[i].neuralnet.weights
        parent.neuralnet.bias = snakes[i].neuralnet.bias
        parents.append(parent)
    children = generate_children(
        parents, population_size - top_old_parents - bottom_old_parents)

    children = mutate(children)
    parents.extend(children)
    return parents


def mutate(children):
    for child in children:
        for weight in child.neuralnet.weights:
            for _ in range(int(weight.shape[0] * weight.shape[1] * mutation_percent/100)):
                row = random.randint(0, weight.shape[0]-1)
                col = random.randint(0, weight.shape[1]-1)
                weight[row][col] += random.uniform(-mutation_intensity,
                                                   mutation_intensity)
    return children


def generate_children(parents, no_of_children):
    all_children = []
    for _ in range(no_of_children):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)

        child = snake.snake(width, height, layers, block_size)
        for i in range(len(parent1.neuralnet.weights)):
            for j in range(parent1.neuralnet.weights[i].shape[0]):
                for k in range(parent1.neuralnet.weights[i].shape[1]):
                    child.neuralnet.weights[i][j, k] = random.choice([
                        parent1.neuralnet.weights[i][j, k],
                        parent2.neuralnet.weights[i][j, k]])

            for j in range(parent1.neuralnet.bias[i].shape[1]):
                child.neuralnet.bias[i][0, j] = random.choice(
                    [parent1.neuralnet.bias[i][0, j],
                     parent2.neuralnet.bias[i][0, j]
                     ]
                )
        all_children.append(child)
    return all_children


def runner():
    '''
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--output', required=True, help="Relative path\
                    to save the snakes")
    args = vars(ap.parse_args())
    '''
    snakes = [snake.snake(width, height, layers,
                          block_size) for _ in range(population_size)]
    playground = Playground(height, width, block_size)
    top_snakes = []
    for i in range(no_of_generations):
        print('generation : ', i+1, ',', end='\n')
        run(snakes, playground)

        snakes.sort(key=lambda x: (
            len(x.snake_position), -x.steps_taken), reverse=True)

        print_top_5(snakes[0:5])

        print('saving the snake')
        top_snakes.append(snakes[0])

        save_top_snakes(top_snakes, "saved/test.pickle")
        snakes = create_new_pop(snakes)


if __name__ == '__main__':
    runner()
