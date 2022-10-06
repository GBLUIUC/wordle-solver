# wordle-solver

## Background

[Wordle](https://www.nytimes.com/games/wordle/index.html) is a fun word guessing game created by Josh Wardle. The rules are as follows:

- Each guess must be a valid 5 letter word.  
- The colors of the tiles will change to show how close your guess was to the word.
  - A green tile means the character is in the word and in the right spot.
  - A yellow tile means the character is in the word but in the wrong spot.  
  - A gray tile means the character is not in the word in any spot. 
 
 
## Usage
`python wordle.py`  

Note: This solver won't help you until after you've made your first guess.

After you submit each guess to Wordle, the solver will prompt you for your guessed word and its associated tags. The text format for tagging uses characters y, m, and n (yes, maybe, no) to represent Green, Yellow, and Gray tiles respectively.  

For example, if your guess was:  
![Wordle guess: Stale with a green box around S, yellow boxes around T and L, and gray boxes around A and E](/images/Stale.png)  

you would input Guess: 'stale' and Tags: 'ymnmn'

## Algorithm

TLDR: This is an Expectation-Maximization problem where 1) the Expectation step prunes the search space based on the tagged guess information and computes conditional probabilities of observing each character and 2) the Maximization step finds the word which maximizes the expected information gain for a guess.

The core heuristic behind the program is making guesses that greedily prune the search space by the maximum amount. In other words, we want to choose the word that will give us the most information gain in expectation. We view any given word as a "bag of characters", independent of positional information. Clearly, this assumption doesn't hold but it simplifies the computation. For every new guess, we compute the conditional probability distribution of each character in our unseen alphabet $\Sigma$ given the information we already have. In other words, for each unseen character $c_i \in \Sigma$, we compute the conditional probability of observing $c_i$ in the solution space $S$ given our knowledge base KB: $P(c_i | KB)$. These conditional probabilities can simply be computed by counting the number of times the character appears in S (with some smoothing): $$P(c_i | KB) = \frac{count(c_i, S) + \delta}{|S| + |\Sigma| * \delta}$$

In reality, the denominator is a constant value and we really only care about the relative ordering of these characters so we just compute the numerator. From these character probabilities, the expected information gain for a given word w is $$Gain(w | KB) = \prod_{c_i \in w} P(c_i | KB)$$ 

and to avoid underflow we use

$$log(Gain(w | KB)) = \sum_{c_i \in w} log( P(c_i | KB) )$$

Using this, we can simply construct candidate guesses that maximize this gain by combining the characters with the highest probabilities to form valid words. One problem with this approach is it will essentially always ignore infrequent characters such as 'Q' until the very end. To account for this, there is an $\epsilon$ chance of including a random letter in the candidate words regardless of frequency.

After the user guesses one of these candidate words, the guess and tag information are used to update the knowledge base and further prune the search space. This approach as it stands is very likely to guess the correct word within 6 tries. However, it is overly conservative and tries to gain information until the solution space is pruned down to a very small number of words (aka it never guesses the solution word until it's extremely confident).

We account for this exploration-exploitation tradeoff by introducing a new heuristic which aims to guess the correct word rather than guessing a word that gives more information. This "Solve" policy is very similar to the "Prune" policy we have so far but we use $\Sigma_{seen}$ rather than $\Sigma_{unseen}$ to generate our guesses. This leverages our existing knowledge base to tailor our guesses toward the solution.  

So our overall policy for suggesting a word is given by $$w_{suggest} =\underset{w}{argmax} \left\((1 - \lambda) \cdot Prune(w | KB) + \lambda \cdot Solve(w | KB) \right)$$ with $\lambda = 1 - e^{-n}$ where n is the number of guesses already made. Intuitively, this means that at the beginning of the game we completely favor exploration but near the end our emphasis is mostly on solving (note that $\lambda$ is never exactly equal to 1 since our solution can still theoretically contain unseen characters).
