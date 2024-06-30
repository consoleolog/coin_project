import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# eth = pd.read_csv('./label_eth.csv')
#
# label = eth.pop('label')
#
# unique_date = eth['date'].unique()
#
# string_lookup_layer = tf.keras.layers.StringLookup(
#     vocabulary=unique_date,
#     num_oov_indices=0,
#     output_mode='one_hot'
# )
# embedding = tf.keras.layers.Embedding(len(unique_date),4)
# date = embedding(string_lookup_layer(unique_date))
#
# normalization_layer = tf.keras.layers.Normalization(mean=2.0, variance=1.0)
#
# close = normalization_layer(tf.constant(eth['close']))
#
# short = normalization_layer(tf.constant(eth['short']))
# middle = normalization_layer(tf.constant(eth['middle']))
# long = normalization_layer(tf.constant(eth['long']))
#
# feature_columns = [
#     date,
#     close,
#     short,
#     middle,
#     long
# ]
#
# ds = tf.data.Dataset.from_tensor_slices((dict(eth), label))
#
# ds_batch = ds.batch(32)
#
# model = tf.keras.models.Sequential([
#     tf.keras.layers.DenseFeatures(feature_columns),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dense(64, activation='tanh'),
#     tf.keras.layers.Dense(32, activation='relu'),
#     tf.keras.layers.Dropout(0.2),
#     tf.keras.layers.Dense(16, activation='tanh'),
#     tf.keras.layers.Dense(8, activation='relu'),
#     tf.keras.layers.Dense(1, activation='sigmoid')
# ])
#
# model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
#
# model.fit(ds_batch, epochs=100, shuffle=True)



eth = pd.read_csv('./label_eth.csv')
label = eth.pop('label')

# Define feature columns
unique_date = eth['date'].unique()

# Define feature columns
date_feature = tf.feature_column.embedding_column(
    tf.feature_column.categorical_column_with_vocabulary_list(
        'date', unique_date), dimension=4)

close_feature = tf.feature_column.numeric_column('close')
short_feature = tf.feature_column.numeric_column('short')
middle_feature = tf.feature_column.numeric_column('middle')
long_feature = tf.feature_column.numeric_column('long')

feature_columns = [
    date_feature,
    close_feature,
    short_feature,
    middle_feature,
    long_feature
]

# Convert DataFrame to dictionary
eth_dict = {col: eth[col].values for col in eth.columns}

# Create a dataset
ds = tf.data.Dataset.from_tensor_slices((eth_dict, label))

ds = ds.batch(32).prefetch(tf.data.experimental.AUTOTUNE)

train, val= train_test_split(ds, test_size=0.2, random_state=42)

# Define the model
model = tf.keras.models.Sequential([
    tf.keras.layers.DenseFeatures(feature_columns),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='tanh'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(16, activation='tanh'),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

tf.keras.utils.plot_model(model, to_file=f'./model_images/model.png',show_shapes=True, show_layer_names=True)

tensorboard = tf.keras.callbacks.TensorBoard(log_dir=f'./logs/model')
es = tf.keras.callbacks.EarlyStopping(
    monitor='accuracy',
    patience=5,
    mode='max',
)

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train, epochs=100, validation_data=val, shuffle=True, callbacks=[es, tensorboard])

model.save('./saved_models/model')