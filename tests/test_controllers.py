
def test_get_user_success(client, mocker):
    mock_user = mocker.Mock()
    mock_user.to_dict.return_value = {"id": 1, "name": "John Doe"}

    mocker.patch('controllers.user_controller.get_users', return_value=[mock_user])
 
    response = client.get('/user/1')

    print('--------------')
    print(response.data)
 
    assert response.status_code == 200
    assert response.json == {"id": 1, "name": "John Doe"}
 
def test_get_user_not_found(client, mocker):
    mocker.patch('controllers.user_controller.get_users', return_value=None)
 
    response = client.get('/user/99')
 
    assert response.status_code == 404
    assert response.json == "User not found"


