import pytest, random, string

from app import app
from datetime import datetime, timedelta

def generar_email_aleatorio():
    dominios = ['gmail.com', 'yahoo.com', 'hotmail.com']
    nombre = ''.join(random.choices(string.ascii_lowercase, k=7))
    dominio = random.choice(dominios)
    return f"{nombre}@{dominio}"

def generar_nombre_aleatorio():
    nombres = ['Carlos', 'Luis', 'María', 'Sofía', 'Ana']
    return random.choice(nombres)

def generar_apellido_aleatorio():
    apellidos = ['García', 'Pérez', 'Rodríguez', 'Martínez', 'López']
    return random.choice(apellidos)

def generar_fecha_nacimiento_aleatoria():
    start_date = datetime.strptime('1940-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2005-12-31', '%Y-%m-%d')
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime('%Y-%m-%d')

@pytest.fixture 
def client():
    app.testing = True
    client = app.test_client()
    return client

def test_insertar_usuario(client):
    nombre = generar_nombre_aleatorio()
    apellido = generar_apellido_aleatorio()
    email = generar_email_aleatorio()
    fechanac = generar_fecha_nacimiento_aleatoria()

    response = client.put('/usuarios', json={'email':email,
                                            'nombre':nombre,
                                            'apellido':apellido,
                                            'fechanac':fechanac})
    json_data = response.json
    assert response.status_code == 200
    assert json_data["message"] == "Usuario creado correctamente"

def test_insertarBuscar_usuario(client):
    email = generar_email_aleatorio()
    nombre = generar_nombre_aleatorio()
    apellido = generar_apellido_aleatorio()
    fechanac = generar_fecha_nacimiento_aleatoria()

    response = client.put('/usuarios', json={'email':email,
                                            'nombre':nombre,
                                            'apellido':apellido,
                                            'fechanac':fechanac})
    json_data = response.json                                            
    if response.status_code == 200 and json_data["message"] == "Usuario creado correctamente":
        response = client.get(f'/usuarios/{email}')
        json_data = response.json
        assert response.status_code == 200
        
        assert json_data['usuarios'][0] == email

def test_borrar_usuario(client):
    response = client.get('/usuarios', json={})
    json_data = response.json
    
    # Obtener la lista de usuarios
    usuarios = json_data['rdo']
    assert response.status_code == 200
    assert json_data["rta"] == 'ok'
    # Asegurarse de que haya al menos un usuario
    if len(usuarios) > 0:    
        # Generar un índice aleatorio entre el primer y el último usuario
        random_index = random.randint(0, len(usuarios) - 1)
        
        usuario_aleatorio = usuarios[random_index]
        email = usuario_aleatorio['email']
        responseDelete = client.delete(f'/usuarios/{email}')
        json_data = responseDelete.json 
        
        assert responseDelete.status_code == 200
        assert json_data['message'] == 'Usuario eliminado correctamente'


