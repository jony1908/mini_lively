from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from passlib.context import CryptContext

from ..database.connection import engine, SessionLocal
from ..config.settings import settings
from ..models.admin_user import AdminUser


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        
        # Try database authentication first
        db = SessionLocal()
        try:
            admin_user = db.query(AdminUser).filter(
                AdminUser.username == username,
                AdminUser.is_active == True
            ).first()
            
            if admin_user and self.pwd_context.verify(password, admin_user.password_hash):
                request.session.update({
                    "admin_user_id": admin_user.id,
                    "admin_username": admin_user.username,
                    "is_superuser": admin_user.is_superuser
                })
                return True
        except Exception as e:
            print(f"Database authentication error: {e}")
        finally:
            db.close()
        
        # Fallback to settings-based authentication
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session.update({
                "admin_user_id": None,
                "admin_username": username,
                "is_superuser": True
            })
            return True
        
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        admin_user_id = request.session.get("admin_user_id")
        admin_username = request.session.get("admin_username")
        return admin_user_id is not None or admin_username is not None


def create_admin(app):
    authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
    
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=authentication_backend,
        title="Mini Lively Admin",
        logo_url=None,
        debug=False,
    )
    
    return admin