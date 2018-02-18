### INSTRUCTIONS TO RUN ###

source venv/bin/activate
python3 Runner.py

If running on windows, it might have path set to python (version 3). In that case run,
python Runner.py

After starting the command, it should start querying the gallows server, and the game should start. It will keep running till the user
interrupts the program.


### DESCRIPTION OF THE SOLUTION ###

The solution uses external DataMuse api (https://www.datamuse.com/api/) to get the search results with words having some set of
characters. It builds on the results returned by the api, to select the next best guess using my algorithm described below:

For example, suppose our Hangman string is 'HIS TRUTH'.
So, our input will be '___ ____'
Since I don't have a point to start, I hit the Hulu api with the most commonly occurring letters, ie 'T' and 'E' (http://letterfrequency.org/)
This gives me a good starting point. My string now is '___ T__T_'

Then, I split the string into words, and for each word, I fetch the most relevant words using the Datamuse api.
The api lets me construct queries searching for words having some characters and of specified length.
Now, these search results need to be ranked to get the next best character guess.
So, I select the top-10 most relevant words (sorted by f-score returned by the api) for each word search.

For example, for 'T__T_' Datamuse api returned (showing only 4 here)
{
    word: "truth",
    score: 2314,
    tags: [
    "f:168.310927"
    ]
},
{
    word: "trite",
    score: 2200,
    tags: [
    "f:1.200587"
    ]
},
{
    word: "taste",
    score: 1727,
    tags: [
    "f:49.705728"
    ]
},
{
    word: "teeth",
    score: 1659,
    tags: [
    "f:55.472105"
    ]
},

Then, I calculate the rank of each distinct character for each word search.
For example, for letter 'h' its score is recorded as 168.310927 + 55.472105
Word complexity = (no of letters known in the word)/(total word length) = 2/5
Now the score for 'h' for this word  = Word complexity x (168.310927 + 55.472105)
Now, I'll get the score for 'h' for each word of Hangman string.

Now final score of 'h' is average of the score of 'h' for each word in Hangman string.

So, I'll do a cumulative rank of all the characters A-Z, and choose the character with top score as the next guess.
For example, our best guess was 'h'. It matched, and the new Hangman string is: 'H__ T__TH'
Then I push 'h' into the list of guessed characters.

This process is repeated till either the status is 'DEAD' or 'FREE'

The code should hopefully be able to predict the correct string for majority of cases.
However, the code might not function optimally, when there are situations where all but one words have been guessed. In that case,
it will start guessing from the start ('A', 'B', 'C' ...) as the word complexity will be 0.

Example - 'FOR EVERYONE IS GOOD' - In this, it guesses FOR, EVERYONE and GOOD correctly, but for IS, it starts guessing from 'A'.
I had a fix in mind, but couldn't implement it because I ran out of time.