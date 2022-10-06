from util import get_guess_tags, findOccurrences, unguess

def main():
    
    unguessed = 'abcdefghijklmnopqrstuvwxyz'

    all_words = []
    sol_words = []
    with open('./data/valid_guesses.csv') as f:
        for line in f:
            all_words.append(line.rstrip())

    with open('./data/valid_solutions.csv') as f:
        for line in f:
            all_words.append(line.rstrip())
            sol_words.append(line.rstrip())

    max_guesses = 6
    num_guesses = 1
    sol_space = sol_words[:]
    guess_space = all_words[:]

    while num_guesses <= max_guesses:

        # Prompt for user input
        print()
        guess, tags = get_guess_tags(all_words)
        if guess == '':
            return
        print()

        # Prune the search space based on the guess
        sol_space, guess_space = prune(guess, tags, sol_space, guess_space)
        unguessed = unguess(guess, unguessed)

        # Check if we've pruned the solution space low enough to guess the answer
        if len(sol_space) == 1:
            print('The solution is: ' + sol_space[0])
            print('And it only took you ' + str(num_guesses + 1) + ' tries!')
            return

        guesses_left = max_guesses - num_guesses
        if len(sol_space) <= guesses_left:
            print('The solution is one of these: ', end='')
            print(sol_space)
            print('You have ' + str(guesses_left) + ' guesses left so just try them all.')
            keep_suggesting = input('Or do you want me to keep helping? (y/n) ').lower()
            if keep_suggesting != 'y':
                return

        # Otherwise, suggest a word that will further prune the space
        suggestions = suggest(sol_space, all_words, unguessed)
        print('I suggest you try to guess the word: ' + suggestions[0])
        see_all = input('Want to see all suggestions? (y/n) ').lower()
        if see_all == 'y':
            print(suggestions)
        
        num_guesses += 1

# Prune the search space based on the tagged information
def prune(guess, tags, sol_space, guess_space):
    pruned_sol = sol_space[:]
    pruned_guess = guess_space[:]

    # First prune out the Y's 
    y_pos = findOccurrences(tags, 'y')
    for pos in y_pos:
        pruned_sol = prune_y(guess, pos, pruned_sol)
        pruned_guess = prune_y(guess, pos, pruned_guess)

    # Now prune out the M's 
    m_pos = findOccurrences(tags, 'm')
    for pos in m_pos:
        pruned_sol = prune_m(guess, pos, pruned_sol)
        pruned_guess = prune_m(guess, pos, pruned_guess)
    
    # Now prune out the N's 
    n_pos = findOccurrences(tags, 'n')
    for pos in n_pos:
        pruned_sol = prune_n(guess, pos, pruned_sol)
        pruned_guess = prune_n(guess, pos, pruned_guess)
    
    return pruned_sol, pruned_guess

def prune_y(guess, pos, search_space):
    pruned = []
    for word in search_space:
        if word[pos] == guess[pos]:
            pruned.append(word)
    return pruned 

def prune_m(guess, pos, search_space):
    pruned = []
    for word in search_space:
        if word[pos] != guess[pos] and guess[pos] in word:
            pruned.append(word)
    return pruned 

def prune_n(guess, pos, search_space):
    pruned = []
    for word in search_space:
        if guess[pos] not in word:
            pruned.append(word)
    return pruned 


# Suggest a ranked list of words with the highest expectation to prune the search space
def suggest(sol_space, guess_space, unguessed):
    char_cand = generate_char_candidates(sol_space, unguessed)
    guess_cands = generate_guess_candidates(char_cand, guess_space, unguessed)
    return guess_cands

# Compute the conditional probabilities of unseen characters to generate a ranked list of candidates
def generate_char_candidates(sol_space, unguessed):
    freq = {}
    for char in unguessed:
        freq[char] = 0
        for word in sol_space:
            if char in word:
                freq[char] += 1

    char_cand = sorted(freq, key=freq.get, reverse=True)
    return char_cand

# Combine candidate characters to generate candidate guesses 
def generate_guess_candidates(char_cand, guess_space, unguessed):

    k = 5
    guess_cands = []
    while k <= len(unguessed):
        guess_cands = []
        for word in guess_space:
            char_cands = char_cand[:k]
            valid = True 
            for char in word:
                if char not in char_cands:
                    valid = False 
                    break
                char_cands.remove(char)
                
            if valid:
                guess_cands.append(word)

        if guess_cands:
            return guess_cands

        k += 1
        
    return ['error'] 




if __name__ == "__main__":
    main()