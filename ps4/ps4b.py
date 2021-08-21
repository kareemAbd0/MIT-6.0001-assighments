# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string


### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print ("Loading word list from file...")
    # inFile: file
    inFile = open (file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend ([word.lower () for word in line.split (' ')])
    print ("  ", len (wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower ()
    word = word.strip (" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open ("story.txt", "r")
    story = str (f.read ())
    f.close ()
    return story


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'


class Message (object):
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''

        self.message_text = text

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        alphanum = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12,
                    'm': 13, 'n': 14, 'o': 15,
                    'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26,
                    'A': 27, 'B': 28, 'C': 29,
                    'D': 30, 'E': 31, 'F': 32, 'G': 33, 'H': 34, 'I': 35, 'J': 36, 'K': 37, 'L': 38, 'M': 39, 'N': 40,
                    'O': 41, 'P': 42, 'Q': 43,
                    'R': 44, 'S': 45, 'T': 46, 'U': 47, 'V': 48, 'W': 49, 'X': 50, 'Y': 51, 'Z': 52}
        new_alphanum = alphanum.copy ()
        final_alphanum = {}
        key_list = list (new_alphanum.keys ())
        val_list = list (new_alphanum.values ())
        n = 1
        for i in new_alphanum.keys ():
            position = val_list.index (n)

            if i.islower ():

                if n + shift <= 26:
                    final_alphanum[i] = key_list[position + shift]
                else:
                    final_alphanum[i] = key_list[position + shift - 26]
            else:
                if n + shift <= 52:
                    final_alphanum[i] = key_list[position + shift]
                else:
                    final_alphanum[i] = key_list[position + shift - 26]
            n += 1
        return final_alphanum





    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        cypherd_message = ""



        cypherd_dect = self.build_shift_dict(shift)
        for x in range (len(self.message_text)):
            if(self.message_text[x] in cypherd_dect.keys()):
                cypherd_message = cypherd_message+cypherd_dect[self.message_text[x]]
            else:
                cypherd_message = cypherd_message+self.message_text[x]
        return cypherd_message







class PlaintextMessage (Message):

    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift



    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift
    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        encryption_dict = super().build_shift_dict(self.shift)
        return encryption_dict
    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        message_text_encrypted = super().apply_shift(self.shift)
        return message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift +=shift





class CiphertextMessage (Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''

        def load_words(file_name):
            '''
            file_name (string): the name of the file containing
            the list of words to load

            Returns: a list of valid words. Words are strings of lowercase letters.

            Depending on the size of the word list, this function may
            take a while to finish.
            '''
            print ("Loading word list from file...")
            # inFile: file
            inFile = open (file_name, 'r')
            # wordlist: list of strings
            wordlist = []
            for line in inFile:
                wordlist.extend ([word.lower () for word in line.split (' ')])
            print ("  ", len (wordlist), "words loaded.")
            return wordlist

        def is_word(word_list, word):

            word = word.lower ()
            word = word.strip (" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
            return word in word_list

        def get_story_string():

            f = open ("story.txt", "r")
            story = str (f.read ())
            f.close ()
            return story

        ### END HELPER CODE ###

        WORDLIST_FILENAME = 'words.txt'
        word_list = load_words (WORDLIST_FILENAME)
        string_list = self.message_text.split()




        right_words_highest = 0
        right_words_temp = 0
        for i in range(26):

           string_list = super().apply_shift(i).split()
           for x in string_list:
               if is_word(word_list,x):

                  right_words_temp +=1

           if right_words_temp >= right_words_highest :
                right_words_highest = right_words_temp
                max = i
                right_words_temp = 0
        best_shifts = (max,super().apply_shift(max))


        return best_shifts






#ex = PlaintextMessage ("help me I AM here!!",4)

#print(ex.get_message_text_encrypted())
#ex2 = CiphertextMessage(ex.get_message_text_encrypted())
#print(ex2.decrypt_message())



if __name__ == '__main__':
        #Example test case (PlaintextMessage)
        plaintext = PlaintextMessage('hello', 2)
        print('Expected Output: jgnnq')
        print('Actual Output:', plaintext.get_message_text_encrypted())

        #Example test case (CiphertextMessage)
        ciphertext = CiphertextMessage('jgnnq')
        print('Expected Output:', (24, 'hello'))
        print('Actual Output:', ciphertext.decrypt_message())

    # TODO: WRITE YOUR TEST CASES HERE
print(get_story_string())
ex2 = CiphertextMessage(get_story_string())
print(ex2.decrypt_message())
    # TODO: best shift value and unencrypted story

