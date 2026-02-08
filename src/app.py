"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "name": "Chess Club",
        "type": "Intellectual",
        "participants": [],
    },
    "Debate Team": {
        "name": "Debate Team",
        "type": "Intellectual",
        "participants": [],
    },
    "Math Olympiad": {
        "name": "Math Olympiad",
        "type": "Intellectual",
        "participants": [],
    },
    "Science Bowl": {
        "name": "Science Bowl",
        "type": "Intellectual",
        "participants": [],
    },
    "Basketball": {
        "name": "Basketball",
        "type": "Sports",
        "participants": [],
    },
    "Soccer": {
        "name": "Soccer",
        "type": "Sports",
        "participants": [],
    },
    "Tennis": {
        "name": "Tennis",
        "type": "Sports",
        "participants": [],
    },
    "Track and Field": {
        "name": "Track and Field",
        "type": "Sports",
        "participants": [],
    },
    "Drama Club": {
        "name": "Drama Club",
        "type": "Artistic",
        "participants": [],
    },
    "Painting Studio": {
        "name": "Painting Studio",
        "type": "Artistic",
        "participants": [],
    },
    "Music Band": {
        "name": "Music Band",
        "type": "Artistic",
        "participants": [],
    },
    "Photography Club": {
        "name": "Photography Club",
        "type": "Artistic",
        "participants": [],
    },
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
