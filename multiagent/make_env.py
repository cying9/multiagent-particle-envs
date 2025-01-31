"""
Code for creating a multiagent environment with one of the scenarios listed
in ./scenarios/.
Can be called by using, for example:
    env = make_env('simple_speaker_listener')
After producing the env object, can be used similarly to an OpenAI gym
environment.

A policy using this environment must output actions in the form of a list
for all agents. Each element of the list should be a numpy array,
of size (env.world.dim_p + env.world.dim_c, 1). Physical actions precede
communication actions in this array. See environment.py for more details.
"""

def make_env(scenario_name, benchmark=False):
    '''
    Creates a MultiAgentEnv object as env. This can be used similar to a gym
    environment by calling env.reset() and env.step().
    Use env.render() to view the environment on the screen.

    Input:
        scenario_name   :   name of the scenario from ./scenarios/ to be Returns
                            (without the .py extension)
        benchmark       :   whether you want to produce benchmarking data
                            (usually only done during evaluation)

    Some useful env properties (see environment.py):
        .observation_space  :   Returns the observation space for each agent
        .action_space       :   Returns the action space for each agent
        .n                  :   Returns the number of Agents
    '''
    from multiagent.environment import MultiAgentEnv
    import multiagent.scenarios as scenarios

    # load scenario from script
    scenario = scenarios.load(scenario_name + ".py").Scenario()
    # create world
    world = scenario.make_world()
    # create multiagent environment
    if benchmark:
        env = MultiAgentEnv(world, scenario.reset_world, scenario.reward,
                            scenario.observation, scenario.benchmark_data)
    else:
        env = MultiAgentEnv(world, scenario.reset_world, scenario.reward,
                            scenario.observation)
    return env


if __name__ == "__main__":
    import numpy as np
    env = make_env("simple_reference")
    act_shape_n = [x.nvec.sum() for x in env.action_space]
    print("N of Agents: ", env.n)
    print("Obs dims: ", [x.shape for x in env.observation_space])
    print("Act dims: ", [x.shape for x in env.action_space])
    print(f"{act_shape_n=}")
    print(f"{env.discrete_action_input=}")
    print(f"{env.force_discrete_action=}")
    print(f"{env.discrete_action_space=}")

    rews = []
    obs = env.reset()
    for step in range(100):
        act_n = [np.random.uniform(size=size) for size in act_shape_n]
        obs2_n, rew_n, done_n, _ = env.step(act_n)
        rews.append(rew_n)
        if all(done_n):
            break
    print(np.array(rews).sum())
