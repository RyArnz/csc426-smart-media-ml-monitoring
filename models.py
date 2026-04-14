from tensorflow import keras
from tensorflow.keras import layers


def build_mlp(input_shape, learning_rate=1e-3):
    """
    Baseline neural model:
    Flatten time window -> Dense(64) -> Dense(32) -> Dense(1)
    """
    model = keras.Sequential(
        [
            layers.Input(shape=input_shape),
            layers.Flatten(),
            layers.Dense(64, activation="relu"),
            layers.Dense(32, activation="relu"),
            layers.Dense(1),
        ]
    )

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="mse",
        metrics=["mae"],
    )
    return model


def build_lstm(input_shape, lstm_units=64, dropout=0.2, learning_rate=1e-3):
    """
    Primary sequence model:
    LSTM -> Dropout -> Dense(16, relu) -> Dense(1)
    """
    model = keras.Sequential(
        [
            layers.Input(shape=input_shape),
            layers.LSTM(lstm_units),
            layers.Dropout(dropout),
            layers.Dense(16, activation="relu"),
            layers.Dense(1),
        ]
    )

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="mse",
        metrics=["mae"],
    )
    return model
