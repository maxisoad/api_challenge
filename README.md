# Football API

## Compose up

```docker-compose up```

## EndPoints

```http://localhost:9090/import-league/<league>```

```http://localhost:9090/total-players/<league>```

## PhpMyadmin

```http://localhost:6030```

User: root - Password: football

## Comments

Flask with Blueprints for the endpoints. MySQL as database.
I choose this framework for its scalability, the simplicity of Flask, it gives us more control of the code, we have to choose each of the libraries we are going to use. This is crucial in the development of critical systems. The framework has to be selected according to the kind of project that has to be developed.
The importation is made in plain sql, in order to improve the performance in this process. This approach gives us more flexibility and control of the queries, and works directly with the database.