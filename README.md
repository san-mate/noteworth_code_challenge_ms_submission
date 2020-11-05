# Noteworth Code Challenge Submition

This repository contains the solution for the challenge presented in [here](https://github.com/datamindedsolutions/noteworth-challenge-api).

## How to run the project:
```
docker-compose up
```

### For the initial build only:

Create initial database:

```
docker-compose run solution python manage.py migrate
```

### Initial Admin User

After running the migrations, you will need to create a "superuser" to access to the Django admin using:

```
docker-compose run solution python manage.py createsuperuser
```

## Usage

To import Clinicians from a provider given, use this command:
```
docker-compose run solution python manage.py import_clinicians <backend_name>
```
- `<backend_name>`: one of the backend names registered (`ALLOWED_IMPORT_BACKENDS`).

For this particular challenge case:
```
docker-compose run solution python manage.py import_clinicians noteworth_challenge_api
```

To see the imported Clinicians you can use the [admin](localhost:8000/admin/clinicians).

### How to run the tests
```
docker-compose run solution python manage.py test providers
```

## Structure

### Clinicians
This package contains mainly the Clinician model, with the idea that it's our own private Clinician, with our own fields and properties. And is also registered into the Django's Admin.

### Providers
This package contains the logic to handle multiple Providers (internally called `backends`) from which the system can pull Clinicians. Currently, there is only one `backend` implemented to retrive Clinicians in `providers.backends.noteworth_challenge.py`, which is extending from `providers.backends.base.BaseImportBackend`, that is the interface to implement when building a new backend. Those backends provide a list of methods:
* `authenticate`: a method that handles the authentication calls to the provider's site.
* `get_auth_header`: a method to get the auth header needed for the new requests to the private API endpoints.
* `get_clinicians`: a method that handles the pulling of Clinicians from the provider's private endpoint, and returns the list obtained.
* `map_to_model_fields`: a method to map field names, that may vary when using different providers, to our own Clinician's field names.

We also store Provider's info in a model called `ProviderToken`, that saves a token and the site url from where it was obtained, so that we can have only one token per site.

The package also contains the management command that handles the import (`import_clinicians`), it takes a `backend_name` as a required param, and you can run it with `--help` to see the available backend names. This command was created with the idea that data imports are scheduled with a crontab job or something similar.

### System configurations

* `noteworth_code_challenge.settings.MAX_API_RETRY`: the amount of times that our backends will retry to get a valid call from the provider's API.
* `providers.backends.__init__.ALLOWED_IMPORT_BACKENDS`: a dict of the backends that can be used to call `import_clinicians`.

## TODOs

* Finish some tests, the method definition is enought to understand what was the idea behind those tests, but some are just passing.
* Use a more robust DB for a "production ready" app, currently is using sqlite.
* Change `backend_name` argument to recive a subclass of `BaseImportBackend` instead of a registered name, to make it more generic and simpler when adding new backends.
* Re-use existing tokens, the current implementation is always doing the auth call and saving a new updated token. It can be improved if we try to get it from our DB at the begining of the `authenticate` method, but this also means that we need to add handling of an invalid token when calling the `/providers` endpoint, to send it back to the auth call.
* Ask somewhere in the command if the Backend provided is actually a subclass of `BaseImportBackend` to enforce the usage of that interface, and also add more checks to the attributes and methods needed for a correctly defined `ImportBackend`.
* Add more debugging info to the logs when getting errors from the provider's API. The command ends gracefully but does not mentiones anything about the amount of tries, the status code, or errors it encounters.
