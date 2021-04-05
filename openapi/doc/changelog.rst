`1.1.11`
--------

- **Fix:** stopped using the internal mechanism of work with CORS because it caused conflicts
- **Fix:** added consumes field to PUT method because there were problems when working with a Swagger

`1.1.10`
--------

- **Fix:** error on logging with info level

`1.1.9`
-------

- **Fix:** error while working with two or more databases

`1.1.8`
-------
- **Fix:** error on creating openapi. namespace record with context presets
- **Fix:** OpenAPI user can't create log records
- **Fix:** wrong handling error in PATCH method
- **Fix:** Error "Object of type datetime is not JSON serializable" in json
  response

`1.1.7`
-------
- **Fix:** Error on opening Setting Dashboard by Admin without OpenAPI access

`1.1.6`
-------
- **Fix:** Slow loading of integration view due to loading logs in python

`1.1.5`
-------
- **Improvement:** namespace's logs displays in standalone tree-view by clicking smart-button

`1.1.4`
-------
- **Fix:** users got same token on installation

`1.1.3`
-------
- **Fix:** don't mark fields as readOnly and required at the same time

`1.1.2`
-------

- **Improvement:** Security rules for reading and configuration

`1.1.1`
-------

- **Fix:** Translation model's float-field into JSON's integer

`1.1.0`
-------

- **New:** search_or_create method is available in all models
- **Improvement:** no need to use extra quotes in context

`1.0.0`
-------

- Init version
