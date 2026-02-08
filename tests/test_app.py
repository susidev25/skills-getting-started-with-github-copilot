"""
Tests for the FastAPI Mergington High School application.
"""
import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Basketball Team" in data
        assert len(data) == 9
    
    def test_activity_has_required_fields(self, client, reset_activities):
        """Test that each activity has required fields."""
        response = client.get("/activities")
        data = response.json()
        activity = data["Chess Club"]
        
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
    
    def test_activity_participants_is_list(self, client, reset_activities):
        """Test that participants field is a list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_new_participant(self, client, reset_activities):
        """Test signing up a new participant for an activity."""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert "newstudent@mergington.edu" in response.json()["message"]
    
    def test_signup_adds_participant_to_list(self, client, reset_activities):
        """Test that signup adds the participant to the activity."""
        email = "newstudent@mergington.edu"
        client.post(f"/activities/Chess Club/signup?email={email}")
        
        # Verify participant was added
        response = client.get("/activities")
        assert email in response.json()["Chess Club"]["participants"]
    
    def test_signup_already_registered_returns_400(self, client, reset_activities):
        """Test that signing up an already registered participant returns 400 error."""
        response = client.post(
            "/activities/Chess Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test that signing up for a nonexistent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_updates_participant_count(self, client, reset_activities):
        """Test that signup updates the participant count correctly."""
        # Get initial count
        response = client.get("/activities")
        initial_count = len(response.json()["Chess Club"]["participants"])
        
        # Sign up new participant
        client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
        
        # Verify count increased
        response = client.get("/activities")
        new_count = len(response.json()["Chess Club"]["participants"])
        assert new_count == initial_count + 1


class TestUnregisterFromActivity:
    """Tests for POST /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_existing_participant(self, client, reset_activities):
        """Test unregistering an existing participant."""
        response = client.post(
            "/activities/Chess Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
    
    def test_unregister_removes_participant(self, client, reset_activities):
        """Test that unregister removes the participant from the activity."""
        email = "michael@mergington.edu"
        client.post(f"/activities/Chess Club/unregister?email={email}")
        
        # Verify participant was removed
        response = client.get("/activities")
        assert email not in response.json()["Chess Club"]["participants"]
    
    def test_unregister_not_registered_returns_400(self, client, reset_activities):
        """Test that unregistering a non-registered participant returns 400."""
        response = client.post(
            "/activities/Chess Club/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test that unregistering from a nonexistent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent Club/unregister?email=test@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_updates_participant_count(self, client, reset_activities):
        """Test that unregister updates the participant count correctly."""
        # Get initial count
        response = client.get("/activities")
        initial_count = len(response.json()["Chess Club"]["participants"])
        
        # Unregister a participant
        client.post("/activities/Chess Club/unregister?email=michael@mergington.edu")
        
        # Verify count decreased
        response = client.get("/activities")
        new_count = len(response.json()["Chess Club"]["participants"])
        assert new_count == initial_count - 1


class TestSignupAndUnregisterFlow:
    """Tests for signup and unregister flow combined."""
    
    def test_signup_then_unregister(self, client, reset_activities):
        """Test signing up and then unregistering a participant."""
        email = "newstudent@mergington.edu"
        
        # Sign up
        response = client.post(f"/activities/Chess Club/signup?email={email}")
        assert response.status_code == 200
        
        # Verify added
        response = client.get("/activities")
        assert email in response.json()["Chess Club"]["participants"]
        
        # Unregister
        response = client.post(f"/activities/Chess Club/unregister?email={email}")
        assert response.status_code == 200
        
        # Verify removed
        response = client.get("/activities")
        assert email not in response.json()["Chess Club"]["participants"]
    
    def test_signup_unregister_unregister_again_returns_error(self, client, reset_activities):
        """Test that unregistering again returns an error."""
        email = "newstudent@mergington.edu"
        
        # Sign up
        client.post(f"/activities/Chess Club/signup?email={email}")
        
        # Unregister
        response = client.post(f"/activities/Chess Club/unregister?email={email}")
        assert response.status_code == 200
        
        # Try to unregister again
        response = client.post(f"/activities/Chess Club/unregister?email={email}")
        assert response.status_code == 400
