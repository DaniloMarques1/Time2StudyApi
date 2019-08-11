## Documentação da api

### Registrar um usuario endpoint -> /registrar.
Recebe um json com os dados do usuario no formato
```json
    {
        "email" : "email@domain",
        "name" : "Nome do usaurio",
        "password" : "senhadosuaurio"
    }
```

### A resposta que a api vai dar será uma mensagem com status code 200 e uma mensagem indicando o sucesso da operação
```json
    {
        "message" : "success"
    }
```
Caso não consiga por algum motivo inserir o usuario retornará 400 com o json seguinte
```json
    {
        "message" : "error"
    }
```

### Endpoint para login -> /logar
O endpoint retornará o token que será utilizado para validação do usuario
```json
    {
        "token" : "token"
    }
```
Em caso de erro na validação do usuario retornará o seguinte json com o código 401
```json
    {
        "message" : "error validating user"
    }
```
### A utilização do token será realizada sempre que precisar de informações sobre o usuario, nesse caso, fazendo uma requisição para o endpoint /user vai obter algumas informações do usuario.
```json
    {
        "email": "danilomarques20@hotmail.com",
        "id_user": 1,
        "name": "Danilo Marques"
    }
```

## Endpoints referentes ao controle das atividades do usuario

### Para adicionar uma task, utilizar o endpoint /addTask passando um json com os valores necessários.
```json
    {
        "title" : "titulo da atividade",
        "description" : "Descrição da atividade a ser realizada",
        "pomodoros_total" : "Quantidade total de pomodoros que será realizada para aquela atividade",
        "id_user" : "Id do usuario ao qual aquela atividade esta vinculada"
    }
```
O retorno será um json com uma mensagem de sucesso e o codigo http 200
```json
    {
        "message" : "success"     
    }
```

### Retornar todas as atividades daquele usuario /tasks enviando o token no header
```json
    {
        "tasks" : [
             {
                "id_task" : "id da task",
                "title" : "titulo da atividade",
                "description" : "Descrição da atividade a ser realizada",
                "current_pomodoros" : "current_pomodoros",
                "pomodoros_total" : "Quantidade total de pomodoros que será realizada para aquela atividade"
            },   
            {
                "id_task" : "id da task",
                "title" : "titulo da atividade",
                "description" : "Descrição da atividade a ser realizada",
                "current_pomodoros" : "current_pomodoros",
                "pomodoros_total" : "Quantidade total de pomodoros que será realizada para aquela atividade"
            }
        ]
    }
```

### Retornar uma task especifica com base no id /task/id
```json
        {
            "id_task" : "id da task",
            "title" : "titulo da atividade",
            "description" : "Descrição da atividade a ser realizada",
            "current_pomodoros" : "current_pomodoros",
            "pomodoros_total" : "Quantidade total de pomodoros que será realizada para aquela atividade"
        }
```

### Atualizar uma tarefa no banco, caso se tenha finalizado um pomodoro. Atualizar a quantidade atual de pomodoros a serem feitas (current_pomodoros) e caso current_pomodoros == pomodoros_total mudar active para 0.