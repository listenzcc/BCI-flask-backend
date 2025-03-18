# Server API

## Startup

The flask server is running on the **waitress-server**.

```powershell
# Run the server
./start-server.ps1
```

## Basic Rule

Support `POST` and `GET` methods, but different with API.

In current stage, it is no need to authenticate.

The successful calling is responded with HTTP response status code with `200`.
The other codes suggest error.
When error, the `msg` parameter is attached for the error message.

```json
// Example of response for good
{'status': 'success', 'body': body}

// Example of response for error
{'status': 'error', 'msg': msg, 'body': body}
```

## Exposed API

### Echo message

The */echo* path echos the input.

### Event stream

The */event-stream* path with `GET` method triggers the stream with date string in 30 times, interval is 30 milliseconds.

### Predict method

The */predict* path with `POST` method requires to predict once.

REQUIRES:
The POST body requires:

- org_id
- user_id
- project_name
- brain_wave_list: it is the wave to be predicted from.
- latest_model_list: the list is assumed to be well sorted with time ascending. And the latest model is used to predict.

The `lates_model` should contain:

- model_path: where the model file is saved.
- checksum: the checksum of the model file.

RESPONSE:
The response is the updated post body:

- pred: The prediction result of the inference.

### Train method

The */train* path with `POST` method requires to train the model.

REQUIRES:
The POST body requires:

- org_id
- user_id
- project_name
- brain_wave_list: it is the wave to be trained from.

RESPONSE:
The response is the updated post body:

- model_path: the path of the model file.
- checksum: the checksum of the model file.
- created_by

## Configuration

The [config.yaml](./config.yaml) is the configuration file.

```yaml
# Project summary
project:
  name: "BCI flask backend"

# Server configuration
connection:
  host: localhost
  port: 7384

# Model configuration
model:
  path: "D:/BCIProject/model"
```
