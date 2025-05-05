from fastapi import APIRouter, Depends, HTTPException
from api.routes.oauth_routes import oauth2_scheme, get_current_user
from api.services.daemon_service import DaemonService, create_daemon
from api.schemas.daemon import DaemonCreationSchema, DaemonIDSchema
from uuid import UUID

daemon_router = APIRouter(prefix="/daemon", tags=["Daemon"])


@daemon_router.get("/all")
async def get_all_daemons(jwt: str = Depends(oauth2_scheme)):
    """
    Get all daemons.
    """

    user = get_current_user(token=jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    daemon = DaemonService.get_all_daemons()
    return {"daemons": daemon}


@daemon_router.get("/{daemon_id}")
async def get_daemon(daemon_id: str, jwt: str = Depends(oauth2_scheme)):
    """
    Get a daemon by ID.
    """
    user = get_current_user(token=jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    try:
        daemon = DaemonService(UUID(daemon_id)).get_daemon()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"daemon": daemon}


@daemon_router.post("/")
async def new_daemon(
    daemon: DaemonCreationSchema, jwt: str = Depends(oauth2_scheme)
):
    """
    Create a new daemon.
    """
    user = get_current_user(token=jwt)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    try:
        daemon = create_daemon(daemon.client_name, daemon.client_secret)
        return {"daemon": daemon}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@daemon_router.delete("/{daemon_id}")
async def delete_daemon(daemon_id:str, jwt: str = Depends(oauth2_scheme)):
    """
    Delete a daemon by ID.
    """
    user = get_current_user(token=jwt)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    try:
        DaemonService(UUID(daemon_id)).delete_daemon()
        return {"status": "success", "message": "Daemon deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
