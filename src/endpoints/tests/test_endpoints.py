def test_get_all_messages_endpoint_returns_200_and_correct_data(client):
    # given
    url = 'api/v1/messages'

    # when
    response = client.get(url, headers={'Content-Type': 'application/json'})

    # then
    assert response.status_code == 200
