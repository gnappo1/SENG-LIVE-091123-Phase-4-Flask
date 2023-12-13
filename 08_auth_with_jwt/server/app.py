#!/usr/bin/env python3

from werkzeug.exceptions import NotFound
from app_setup import app, db, api, jwt
from models.user import User
from routes.crew_member_by_id import CrewMemberById
from routes.crew_members import CrewMembers
from routes.production_by_id import ProductionById
from routes.productions import Productions
from routes.welcome import Welcome
from routes.auth.signup import Signup
from routes.auth.login import Login
from routes.auth.me import Me
from routes.auth.refresh import Refresh
from routes.auth.check_token import CheckToken
#! Routes
api.add_resource(Welcome, "/")
#! GET/POST Productions routes
api.add_resource(Productions, "/productions")
#! GET/PATCH/DELETE Production routes
api.add_resource(ProductionById, "/productions/<int:id>")
#! GET/POST CrewMembers routes
api.add_resource(CrewMembers, "/crew_members")
#! GET/PATCH/DELETE CrewMembers routes
api.add_resource(CrewMemberById, "/crew_members/<int:id>")
#! POST Signup
api.add_resource(Signup, "/signup")
#! POST Login
api.add_resource(Login, "/login")
#! GET Me
api.add_resource(Me, "/me")
#! POST Refresh
api.add_resource(Refresh, "/refresh")
#! GET Check Token
api.add_resource(CheckToken, "/check")
#! No need for a logout route in this configuration!

# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return db.session.get(User, identity)


#! Global Error Handling
@app.errorhandler(NotFound)  #! 404
def handle_404(error):
    response = {"message": error.description}
    return response, error.code


if __name__ == "__main__":
    app.run(debug=True, port=5555)
