
from unittest.mock import PropertyMock, patch
from controllers.user_controller import *


def test_list_users_success(mocker,client):
    mock_user1 = mocker.Mock()
    mock_user2 = mocker.Mock()

    mock_users = [mock_user1,mock_user2]

    mock_user1.to_dict.return_value = {"id": 1, "name": "user1"}
    mock_user2.to_dict.return_value = {"id": 2, "name": "user2"}

    mocker.patch('routes.user_route.get_users', return_value=mock_users)

    response = client.get('/user')

    # print(response.data)

    assert response.status_code == 200
    assert response.json == [{"id": 1, "name": "user1"},
                  {"id": 2, "name": "user2"}]

def test_list_users_not_found(mocker,client):
    mocker.patch('routes.user_route.get_users', return_value=None)
    response = client.get('/user')

    assert response.status_code == 404
    assert response.json == "No users found"



def test_get_user_success(client, mocker):
    mock_user = mocker.Mock()
    mock_user.to_dict.return_value = {"id": 1, "name": "user1"}

    mocker.patch('routes.user_route.get_users', return_value=[mock_user])
 
    response = client.get('/user/1')

    assert response.status_code == 200
    assert response.json == {"id": 1, "name": "user1"}
 
def test_get_user_not_found(client, mocker):
    mocker.patch('routes.user_route.get_users', return_value=None)
 
    response = client.get('/user/99')
 
    assert response.status_code == 404
    assert response.json == "User not found"



def test_add_user_success(client, mocker):
    mock_user = mocker.Mock()
    mock_user.to_dict.return_value = {"id": 1, "name": "user1"}
    mocker.patch('routes.user_route.add_user', return_value=mock_user)

    data = {'name':'user1'}
    response = client.post('/user',data=data)

    assert response.status_code == 200
    assert response.json == {"id": 1, "name": "user1"}

def test_add_user_bad_request(client, mocker):
    data = {'name':''}
    response = client.post('/user',data=data)
    assert response.status_code == 400
    assert response.json == {"errors":['name is empty']}


def test_delete_user_success(client, mocker):
    mock_user = mocker.Mock()
    type(mock_user).id = PropertyMock(return_value=1)

    mocker.patch('routes.user_route.delete_user', return_value=mock_user)
    
    response = client.delete('/user/1')

    assert response.status_code == 200
    assert response.json == f'user 1 deleted'

def test_delete_user_not_found(client, mocker):
    mocker.patch('routes.user_route.delete_user', return_value=None)
 
    response = client.delete('/user/99')
 
    assert response.status_code == 404
    assert response.json == "User not found"


def test_update_user_success(client, mocker):
    mock_user = mocker.Mock()
    type(mock_user).id = PropertyMock(return_value=1)

    mocker.patch('routes.user_route.update_user', return_value=mock_user)

    data = {'name':'user2'}
    response = client.patch('/user/1',data=data)

    assert response.status_code == 200
    assert response.json == f'user 1 updated'

def test_update_user_bad_request(client, mocker):
    data = {'name':''}
    response = client.post('/user',data=data)
    assert response.status_code == 400
    assert response.json == {"errors":['name is empty']}


