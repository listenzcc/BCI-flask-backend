# Machine learning algorithms

The [util.py](./util.py) file contains the model training and predicting methods.
And it saves and loads the model files.

## Model storage and caching

The `inventory_path` is the folder where the model files are saved.
Each file is a binary file.

- The name of the file is randomly and unique with info, creating time and random value.
- The file contains both the `model` object and `info` dictionary.
- During saving the file, the **checksum** of the file is calculated and passed.

The filename is in the format of md5 and the **checksum** is generated with the binary files's sha256 hash.

The `ModelCache` class provides the rapid caching during prediction.
The cache prevents the model from being loaded repeatedly.
The cache key is the **checksum** of the model file.

- When the prediction request is initially triggered, the file is loaded with checksum checking. (which ensures the model file is correct.)
- The `prepare_model` does the caching job.
- The model and info are cached after the first loading.
- The succeeding prediction uses the cached model instead loading the model again.

## Model training & inference (prediction)

The `train` method is used to train the model, with X and y are known.
The `info` dictionary contains the subject's information, and it is saved into the binary file with the trained model.

The `predict` method is used to predict the y using given X.
The `checksum` is required to located the cached model. (which requires `prepare_model` finished in advance.)

Moreover, the training and inference must be surely compatible.
