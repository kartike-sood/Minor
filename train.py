from preprocessing import generating_training_sequences, sequence_length
import keras

OUTPUT_UNITS = 18 # Number of items in our mappings dictionary
NUM_UNITS = [256] # we are passing it as a list because the LSTM layer can have more than 1 hidden layer
LOSS = "sparse_categorical_crossentropy" # Loss function
LEARNING_RATE = 0.001 # Learning rate of the model

def build_model(output_units, num_units, loss, learning_rate):

    # create the model architecture
    input = keras.layers.Input(
         shape = (None, # written "None" here as it enables us to use this layer as many times as we require.
                 output_units # it specifies the number of neurons in the LSTM
                 )
                )

    x = keras.layers.LSTM(num_units[0])(input)
    x = keras.layers.Dropout(0.2)(x)

    output = keras.layers.Dense(ouput_units, activation = "softmax")(x)


    # compile the model



def train(output_units = OUTPUT_UNITS, num_units = NUM_UNITS, loss = LOSS, learning_rate = LEARNING_RATE):

    # generate the training sequences
    inputs, targets = generating_training_sequences(sequence_length)

    # build the LSTM Neural Network
    model = build_model(output_units, num_units, loss, learning_rate)

    # train the model


    # save the model