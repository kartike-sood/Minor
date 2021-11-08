import tensorflow.keras as keras
import json
import numpy as np
from tensorflow.python.keras.backend import one_hot
from preprocessing import SEQUENCE_LENGTH, MAPPING_PATH
from train import SAVE_MODEL_PATH

class MelodyGenerator:


    def __init__(self, model_path = SAVE_MODEL_PATH):
        
        self.model_path = model_path
        self.model = keras.models.load_model(model_path)
        
        with open(MAPPING_PATH, "r") as fp:
            self._mappings = json.load(fp)

        self._start_symbols = ["/"] * SEQUENCE_LENGTH


    def generate_melody(self, seed, num_steps, max_sequence_length = SEQUENCE_LENGTH, temperature = 0.7):

        seed = seed.split() # converting the seed to a list of notes and rests

        melody = seed

        # I don't know yet why we have added 64 '/' symbols in the start of the seed
        seed = self._start_symbols + seed

        # map seed to int
        seed = [self._mappings[symbol] for symbol in seed]

        for _ in range(num_steps):

            # We are doing this because our model can take 64 symbols at a time to give the output
            seed = seed[-max_sequence_length : ]

            # one-hot encoding the seed because our model has been trained in the same way
            one_hot_seed = keras.utils.to_categorical(seed, num_classes = len(self._mappings))

            # adding another dimension to the seed because keras accepts an extra dimension
            # current dimension of seed -> max_sequence * len(mappings)
            # desired dimension of seed -> 1 * max_sequence * len(mappings)
            one_hot_seed = one_hot_seed[np.newaxis, ...]

            # Making a prediction

            # We are taking only the 0th index because our model will output a batch of outputs had we passed
            # in a batch of seeds but since we have passed only 1 seed, hence we will extract the first and
            # only item in the output list

            probabilities = self.model.predict(one_hot_seed)[0]

            """
            We will get a list of probabilities from this statement like :
            [0.2, 0.3, .... 0.1, 0.1, 0.2] ( total 18 elements[len(mappings)] )
            which will add up to give 1.

            One way to proceed from here is to get the most probable outcome an set it as output for the 
            input seed, but in that way we will be getting very rigid outputs.
            
            For example : if the most probable outcome for "I don't ..." is "know" then for everytime,
            the words "I don't" are encountered, the answer will always be "know" and then there will be
            no possibility of nuances in the output of our model.

            For reading more about it, go to https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277
            """

            output_int = self._sample_with_temperature(probabilities, temperature)

            # update the seed
            seed.append(output_int)

            # map the integers back to the midi values
            key_list = self._mappings.keys()
            val_list = self._mappings.values()

            position = val_list.index(output_int)

            output_symbol = key_list[position]

            if(output_symbol == '/'):
                break

            melody.append(output_symbol)

        return melody

    def _sample_with_temperature(self, probabilities, temperature):

        predictions = np.log(probabilities) / temperature
        probabilities = np.exp(predictions) / np.sum(np.exp(predictions))

        choices = range(len(probabilities))
        index = np.random.choice(choices, p = probabilities)

        return index

if __name__ == "__main__":

    mg = MelodyGenerator()
    seed = "64 _ 69 _ _ _ 71 _ 72 _ _ 71 69 _ 76"

    melody = mg.generate_melody(seed, num_steps = 500, max_sequence_length = SEQUENCE_LENGTH, temperature = 0.7)
    print(melody)