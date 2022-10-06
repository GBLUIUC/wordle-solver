# Prompt the user for input
def get_guess_tags(all_words):
    guess = ''
    tags = ''

    while guess not in all_words:
        guess = input('Guess: ').lower()
        if guess == 'quit':
            return '', ''
        if guess not in all_words:
            print('Invalid guess; try again (or type quit to exit)\n')

    valid_tags = False
    while not valid_tags:
        tags = input('Tags: ').lower()
        if tags == 'quit':
            return '', ''
        valid_tags = validate_tags(tags)
        if not valid_tags:
            print('Invalid tags; try again (or type quit to exit)\n')
    
    return guess, tags

# Validate tags: should be length 5 and only contain y m or n
def validate_tags(tags):
    if len(tags) != 5:
        return False 
    for char in tags:
        if char not in 'ymn':
            return False 
    return True

# Returns the indices of all occurences of char c in string s
def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

# Remove all characters in guess from unguessed
def unguess(guess, unguessed):
    for char in guess:
        unguessed = unguessed.replace(char, '')
    return unguessed

