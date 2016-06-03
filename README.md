# MCMC Part 1: Boolean

 
This is the first part of two labs to be done INDIVIDUALLY (no groups). As discussed in class, write a program to implement Gibs sampling. Your code will evetually need to use Metropolis Hastings (or just Metropolis) to handle continuous nodes but that is in the next part of the lab, take a look at that lab so you know where you are headed. For now you only need to handle Bernoulli nodes.

Please demonstrate your code on the networks given below AND on one you make up yourself. Share the network you make up by posting it (and a query) on the discussion page (called "Digital Dialog" in Learning Suite) BUT DO NOT POST THE ANSWER. Run your code on a couple of networks that have be posted by others.

Because of numerical issues, we strongly recommend doing calculations on the log scale.

Please submit a report on your code that is complete enough that I can see what you have done without having to run your code, although you need to submit the code too. Include your answers from the tests below, and from the discussion page. Include some mixing plots and, of course, prior and posterior plots for each example (the point isn't to see how many trees you can kill) but again, you must demonstrate that your code worked and got the right distributions.

## Example Networks
### Burglar Alarm
The Burglar Alarm example is described in Russell and Norvig's book "Artificial Inteligence a Modern Apporach". If you don't have the book, look at slides 5 and 6 on this pdf. This network involves only discrete nodes.

The model probabilities are:
> P(Burglary=true) = 0.001
P(Eathquake=true) = 0.002
P(Alarm=true | Burglary=true, Earthquake=true) = 0.95
P(Alarm=true | Burglary=true, Earthquake=false) = 0.94
P(Alarm=true | Burglary=false, Earthquake=true) = 0.29
P(Alarm=true | Burglary=false, Earthquake=false) = 0.001
P(JohnCalls=true | Alarm=true) = 0.90
P(JohnCalls=true | Alarm=false) = 0.05
P(MaryCalls=true | Alarm=true) = 0.70
P(MaryCalls=true | Alarm=false) = 0.01

According to Russell and Norvig:
 

> P(Burglary | JohnCalls=true, MaryCalls=true) = <0.284, 0.716>

Simulation should give a similar answer.
Our code reported the following results as well:

>P(Alarm | JohnCalls=true, MaryCalls=true) = <0.75, 0.25>
P(Earthquake | JohnCalls=true, MaryCalls=true) = <0.17, 0.83>
P(Burglary | JohnCalls=false, MaryCalls=false) = <0.00, 1.00>
P(Burglary | JohnCalls=true, MaryCalls=false) = <0.01, 0.99>
P(Burglary | JohnCalls=true) = <0.02, 0.98>
P(Burglary | MaryCalls=true) = <0.05, 0.95>
 
## Notes:

- You should not need to use much from any statistics libraries. Really all you need to be able to do is to sample from a bernoulli.
- Try to keep your code somewhat general. You really should not have to have a separate Metropolis implementation for each different type of node.
- For Bernoulli/Binomial, sample directly instead of trying to use Metropolis.

#  Learning Lab

This lab should be done in pairs. Try these experiments using both versions of you MCMC code.
 
## Faculty data

I have updated the specification given below. I have tried to be more clear about what plots are required. I still want you to experiment. Find something you think is interesting to show.
Experiment with parameter learning in the faculty data from the mcmc lab:
Add hyper-parameters and learn them one-by-one. Compare your results as you go.
How does learning the hyper-parameters affect the posterior distributions for the mean and variance? Compare the posterior distributions you obtain with learned hyper-parameters to the posterior distributions you obtained when the prior parameters (hyper-parameters) were hard coded.
In the end you should have four graphs for the mean and variance (hint: one joint mean variance graph is better than two independent ones) and one for the hard coded hyper-parameters. You will also need a few graphs of the distributions over the hyper parameters for each case (hint: one graph with multiple lines is easier to draw conclusions from than several independent graphs). You will need to check the mixing with mixing graphs, but you do not need to show them to me.

## Alarm Model

Extend the Alarm model from the mcmc lab to allow for multiple observations and parameter learning. However we will modify it as follows:

>P(b)=0.2 and P(e)= 0.3 (think of them as lifetime probabilities or the author has moved to a very unstable neighborhood...)
P(a|~b,~e) = 0.2 (bad alarm too...)
P(j|~a) = 0.2 and P(m|~a) = 0.3 (but friendlier neighbors!)

In this case generate your own test data (hint: generating data is like inference, just the knows and unknowns trade places, you should be able to use your mcmc code!). Try the following:
Add three hyper-parameters to learn, then try learning with 1/2 of the parameters, then try learning them all. The point is to get a feel for how adding hyper-parameters affects your network. Compare your results as you go, and compare your results to the known true parameters.
Experiment with the amount of data you give your parameter learning version of the network. Note that your objective here is to see how data affect the learning. Obviously more data allows you to better learn the parameters. Unfortunately more data will take longer too. Do not get carried away with the amount of data or you will spend the rest of the semester on this! You might want to start with just 100 sets of observations, you may need to go even lower. Show me a few plots so I can see a change in the learning as you changed the amount of data.
Experiment with the true parameters. For example, go back to the original parameters (P(b)= 0.001, etc.), does this make the system harder or easier to learn? What in general makes a net harder to learn? (a few more plots)
Add a hyper-hyper-parameter or two. How does this affect your results. (one or two more plots)
Putting it all together:
You do not need to include the hyper-hyper parameters for the following part:
Try adding some observations with missing data (removed by hand if that is easiest for you). For example, suppose for some rows in your input data, you do not know if John Called or not, in others we do not know if there was a burglary or not. Again, remove a large enough percentage of the data so I can see a change in the learning. (a few plots)
Add inference: Given a batch of your data, assume that Mary has just called. What is the posterior probability of a burglary given your training data and the fact that Mary called. (one more plot)
Change the parameters and generate some data (with missing data). Post you data on the wiki. In your report tell ME what the parameters are so I can compare the true values with the values learned by your classmates (ON THE BURGLARY AND ALARM NODES ONLY).
Re-run your learner (with all hyper parameters, but no hyper-hyper-parameters) with data from another group that has been posted on the wiki. Report on your results by plotting the distributions of the hyper parameters ON THE BURGLARY AND ALARM NODES ONLY.

## Report

In general I would like to see a lot of graphs and not much writing. What writing you do should be pointing out the interesting things about the graphs and drawing conclusions.
Note that you can go back to working in pairs for this lab. Since you will each have your own mcmc code, you might want to try running a few of your experiments on both versions and comparing the results.
 

