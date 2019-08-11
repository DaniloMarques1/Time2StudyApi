
## API

### Endpoint - /api/registrar
Responsavel pelo registro de um usuario. Recebera -> name, email, password
retornará um json no formato
```json
{
    "success" : "Boolean"
}
```

### Endpoint - /auth
Responsável pela geração do token. Irá gerar um token para o usuario em caso de haver um registro do usuario passado no banco de dados. Recebe na requisição o email e a senha do usuario. O token ficará guardado no lado do cliente no localStorage.

```json
{
    "access_token" : "token"
}

```
Em caso de email/senha inválidos, ele retornará:
```json
{
    "description": "Invalid credentials",
    "error": "Bad Request",
    "status_code": 401
}
```

### Endpoint - /api/getUser
Responsavel por retornar informações sobre o usuario logado, utilizará o token para validação (@jwt_required()).

```json
{
    "id" : "user_id",
    "name" : "user_name",
    "email" : "user_email"
    
}
```
Caso o token de validação tenha se expirado no lado do cliente será necessário a geração de um novo (logar novamente)
```json
{
    "description": "Signature has expired",
    "error": "Invalid token",
    "status_code": 401
}
```
Se por algum motivo o token foi modificado no lado do cliente e ele tentar passar o token incorreto:
```json
{
    "description": "Signature verification failed",
    "error": "Invalid token",
    "status_code": 401
}
```

## Abaixo segue os endpoints que tratam as atividades
### Endpoint - /api/viewTasks
Vai retornar todas as tasks que não foram finalizadas de um determinado usuario. Receberá o id o usuario.
Retorno:
```json
{
    "tasks" : [
                "task1", 
                "task2", 
                "task3",
                "task4"]
}
```
Onde task1 -> é uma lista -> task1[0] -> id_task, task1[1] -> id_user, task2[2] -> Titulo, task2[3] -> Qtd_pomodoros, task2[4] -> Descrição

### Endpoint - /api/addTask
Endpoint para adicionar uma nova atividade, receberá o id do usuario logado e as informações sobre a atividade. E efetuara a inserção da atividade no banco.
