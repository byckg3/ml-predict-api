import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import create_autospec

from app.api.auth.dependencies.csrf_utils import create_csrf_token
from app.api.auth.dependencies.jwt_utils import create_access_token
from app.api.dependencies.service import user_service
from app.main import app
from app.user.services import UserService
from app.user.v2.schemas import UserProfile, examples

base_path = "/api/v2/user"


@pytest.fixture
def mock_user_service():
    mock_service = create_autospec( UserService, instance = True )
    
    mock_service.find_by_id.return_value = None
    app.dependency_overrides[ user_service ] = lambda: mock_service
    
    yield mock_service
    
    # app.dependency_overrides.clear()
    del app.dependency_overrides[ user_service ]


@pytest.fixture( scope = "module" )
def client():
    
    jwt_token = create_access_token( payload = examples[ "base_profile" ] )
    csrf_token = create_csrf_token()
    
    auth_cookies = { "csrf_token": csrf_token }
    auth_headers = { "Authorization": f"Bearer {jwt_token}",
                "X-CSRF-Token": csrf_token  }
    
    with TestClient( app = app, 
                     cookies = auth_cookies, 
                     headers = auth_headers ) as client:
        yield client


# @pytest.mark.test_only
def test_get_profile_not_found( client, mock_user_service ):
	
	response = client.get( url = f"{ base_path }/profile/test-id" )

	assert response.status_code == status.HTTP_404_NOT_FOUND


# @pytest.mark.test_only
def test_user_crud_flow( client: TestClient ):
    
    # save profile
    response = client.post(
        f"{ base_path }/profile",
        json = examples[ "base_profile" ],
    )
    payload: dict = response.json()
    
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" not in payload
    assert payload[ "public_id" ] is not None


    # update profile
    updated_name = "Updated Name"
    response = client.put(
        f"{ base_path }/profile/{ payload[ "public_id" ] }",
        json = { "name": updated_name },
    )
    user_profile = UserProfile.model_validate( response.json() )

    assert response.status_code == status.HTTP_200_OK
    assert user_profile.updated_at > user_profile.created_at
    

    # get profile
    response = client.get( f"{ base_path }/profile/{ payload[ "public_id" ] }" )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[ "name" ] == updated_name
    
    
    # delete profile
    response = client.delete( f"{ base_path }/profile/{ payload[ "public_id" ] }" )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    

# @pytest.mark.test_only
def test_save_profile_with_invalid_input( client: TestClient ):
    response = client.post(
        f"{ base_path }/profile",
        json = {
            "name": "John Doe",
            "email": "invalid-email-format"
        },
    )
    # json = response.json()
    # print(json)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT