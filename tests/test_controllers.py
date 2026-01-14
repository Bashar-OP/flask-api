
def test_list_users_success(client, mocker):
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
 
def test_list_users_not_found(client, mocker):
    mocker.patch('routes.user_route.get_users', return_value=None)
 
    response = client.get('/user/99')
 
    assert response.status_code == 404
    assert response.json == "User not found"



def test_get_user_success(client, mocker):
    mock_user = mocker.Mock()
    mock_user.to_dict.return_value = {"id": 1, "name": "John Doe"}

    mocker.patch('routes.user_route.get_users', return_value=[mock_user])
 
    response = client.get('/user/1')

    assert response.status_code == 200
    assert response.json == {"id": 1, "name": "John Doe"}
 
def test_get_user_not_found(client, mocker):
    mocker.patch('routes.user_route.get_users', return_value=None)
 
    response = client.get('/user/99')
 
    assert response.status_code == 404
    assert response.json == "User not found"







