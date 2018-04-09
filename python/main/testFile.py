from matplotlib import pyplot as plt
from agent import environment_set

env = environment_set.Tracker()
observation = env.reset()
# print(observation)
for _ in range(2):
    for _ in range(50):
        observation, reward, done, info = env.step(env.action_space.sample())
        # print(observation)
        plt.plot(observation)
    print("ran")
    observation = env.reset()
    # plt.show()
    print('\n')

env.close()