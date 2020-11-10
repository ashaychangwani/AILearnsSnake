import random
import pickle
import time
from boundary import Environment
import snake
import numpy as np
import matplotlib.pyplot as plt


class GeneticAlgo:

    def __init__(self, width, height, unit, NN_shape, init_NN, population_size, no_of_generations,
                 per_of_best_old_pop, per_of_worst_old_pop, mutation_percent, mutation_intensity):

        self.width = width
        self.height = height
        self.unit = unit
        self.NN_shape = NN_shape
        self.init_NN = init_NN
        self.population_size = population_size
        self.no_of_generations = no_of_generations
        self.per_of_best_old_pop = per_of_best_old_pop
        self.per_of_worst_old_pop = per_of_worst_old_pop
        self.mutation_percent = mutation_percent
        self.mutation_intensity = mutation_intensity

    def run(self, snakes, environment):

        i = 1
        scores = []

        generation_seed = random.random()
        for snake in snakes:
            start_time = time.time()
            checkloop = False
            self.progress(i/self.population_size, 30)
            random.seed(generation_seed)
            apple_position = environment.create_new_apple(snake.snake_position)
            snake.neuralnet.setNextFood(apple_position)

            while(snake.isAlive()):
                if (snake.head_x, snake.head_y) == environment.apple_position:
                    snake.time_since_apple = 0
                    result = snake.neuralnet.decision(
                        snake.head_x, snake.head_y, snake.snake_position, snake.direction)
                    snake.eatApple(result)
                    start_time = time.time()
                    snake.neuralnet.setNextFood(
                        environment.create_new_apple(snake.snake_position))
                    checkloop = False

                if snake.time_since_apple > 250:  # could be tuned
                    if not checkloop:
                        checkloop = True
                        any_point_of_loop = (snake.head_x, snake.head_y)
                        times = 0
                    elif (snake.head_x, snake.head_y) == any_point_of_loop:
                        times += 1
                        if times > 2:
                            snake.collision_with_boundary = True
                            snake.collision_with_self = True

                if time.time() - start_time > 0.5:
                    snake.collision_with_boundary = True
                    snake.collision_with_self = True

                result = snake.neuralnet.decision(
                    snake.head_x, snake.head_y, snake.snake_position, snake.direction)

                if snake.move(result) == False:
                    break
            random.seed()
            scores.append(len(snake.snake_position) - 1)
            i += 1
        print("\nAverage: %.2f \n90th percentile: %.2f" %
              (np.average(scores), np.percentile(scores, 90)))
        return np.average(scores), np.percentile(scores, 90)

    def print_top(self, snakes):
        i = 0
        for snake in snakes:
            i += 1
            print('snake ', i, ', score : ', len(snake.snake_position)
                  - 1, end='\t')
            if snake.collision_with_self and snake.collision_with_boundary:
                print('stuck in loop')
            elif snake.collision_with_boundary and not snake.collision_with_self:
                print('crashed wall')
            else:
                print('crashed body')

    def save(self, snakes, filename):
        f = open(filename, "wb")
        pickle.dump(snakes, f)
        f.close()

    def cloneOfParents(self, parents):
        snakes = []
        for parent in parents:
            babySnake = snake.snake(self.width, self.height,
                                    self.NN_shape, self.unit,
                                    False)
            babySnake.neuralnet.theta = parent.neuralnet.theta
            babySnake.neuralnet.bias = parent.neuralnet.bias
            snakes.append(babySnake)
        return snakes

    def elitism(self, snakes):
        parents = []
        num_top = int(self.population_size *
                              self.per_of_best_old_pop / 100)
        num_bottom = int(self.population_size *
                                 self.per_of_worst_old_pop / 100)

        parents.extend(self.cloneOfParents(snakes[:num_top]))
        parents.extend(self.cloneOfParents(snakes[-num_bottom:]))
        return parents, num_top, num_bottom
    
    def create_new_pop(self, snakes):
        parents, num_top, num_bottom = self.elitism(snakes)
        children = self.offspringGeneration(
            parents, self.population_size - num_top - num_bottom)

        children = self.mutate(children)
        parents.extend(children)
        return parents

    def crossOver(self, parent1, parent2):
        child = snake.snake(self.width, self.height,
                            self.NN_shape, self.unit)
        for i in range(len(parent1.neuralnet.theta)):
            for j in range(parent1.neuralnet.theta[i].shape[0]):
                for k in range(parent1.neuralnet.theta[i].shape[1]):
                    child.neuralnet.theta[i][j, k] = random.choice([
                        parent1.neuralnet.theta[i][j, k],
                        parent2.neuralnet.theta[i][j, k]])

            for j in range(parent1.neuralnet.bias[i].shape[1]):
                child.neuralnet.bias[i][0, j] = random.choice(
                    [parent1.neuralnet.bias[i][0, j],
                        parent2.neuralnet.bias[i][0, j]
                     ]
                )
        return child

    def offspringGeneration(self, parents, no_of_children):
        all_children = []
        for _ in range(no_of_children):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)

            all_children.append(self.crossOver(parent1, parent2))

        return all_children

    def mutate(self, children):
        for child in children:
            for W in child.neuralnet.theta:
                for _ in range(int(W.shape[0] * W.shape[1] * self.mutation_percent/100)):
                    row = random.randint(0, W.shape[0]-1)
                    col = random.randint(0, W.shape[1]-1)
                    W[row][col] += random.uniform(-self.mutation_intensity,
                                                  self.mutation_intensity)
        return children

    def runner(self):
        snakes = [snake.snake(self.width, self.height, self.NN_shape,
                              self.unit) for _ in range(self.population_size)]
        environment = Environment(self.height, self.width, self.unit)
        top_snakes = []
        averages = []
        percentile = []
        for i in range(self.no_of_generations):
            print('GENERATION: ', i+1, end='\n')
            avg, ptile = self.run(snakes, environment)
            averages.append(avg)
            percentile.append(ptile)

            snakes.sort(key=lambda x:
                len(x.snake_position), reverse=True)

            self.print_top(snakes[0:5])

            top_snakes.append(snakes[:3])

            snakes = self.create_new_pop(snakes)
        self.save(top_snakes, "saved/test.pickle")
        plt.plot(averages)
        plt.plot(percentile)
        plt.show()

    def progress(self, percent, length):
        hashes = round(percent*length)
        print('\r', '*'*hashes + '_'*(length - hashes),
              '[{:.2%}]'.format(percent), end='')


if __name__ == '__main__':
    width = 540
    height = 440
    unit = 10
    NN_shape = [24, 16, 3]
    init_NN = True
    population_size = 50
    no_of_generations = 30
    per_of_best_old_pop = 20.0  # percent of best performing parents to be included
    per_of_worst_old_pop = 2.0  # percent of worst performing parents to be included
    mutation_percent = 7.0
    mutation_intensity = 0.1

    ga = GeneticAlgo(width, height, unit, NN_shape, init_NN, population_size, no_of_generations,
                     per_of_best_old_pop, per_of_worst_old_pop, mutation_percent, mutation_intensity)

    ga.runner()