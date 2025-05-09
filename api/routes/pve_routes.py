from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from api.db import get_db
from api.schemas import pve as schemas
from api.services.pve import PveService
from uuid import UUID

pve_router = APIRouter(prefix="/pve", tags=["PVE"])


@pve_router.post(
    "/clusters", response_model=schemas.ClusterOut, status_code=status.HTTP_201_CREATED
)
async def create_cluster(data: schemas.ClusterCreate, db: Session = Depends(get_db)):
    try:
        return PveService.create_cluster(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@pve_router.get("/clusters", response_model=List[schemas.ClusterOut])
async def list_clusters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return PveService.list_clusters(db, skip, limit)


@pve_router.get("/clusters/{cluster_id}", response_model=schemas.ClusterOut)
async def get_cluster(cluster_id: str, db: Session = Depends(get_db)):
    cluster_id = UUID(cluster_id)
    cluster = PveService.get_cluster(db, cluster_id)
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return cluster


@pve_router.patch("/clusters/{cluster_id}", response_model=schemas.ClusterOut)
async def update_cluster(
    cluster_id: str, data: schemas.ClusterUpdate, db: Session = Depends(get_db)
):
    cluster_id = UUID(cluster_id)
    updated = PveService.update_cluster(db, cluster_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return updated


@pve_router.delete("/clusters/{cluster_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cluster(cluster_id: str, db: Session = Depends(get_db)):
    cluster_id = UUID(cluster_id)
    if not PveService.delete_cluster(db, cluster_id):
        raise HTTPException(status_code=404, detail="Cluster not found")


@pve_router.post(
    "/nodes", response_model=schemas.NodeOut, status_code=status.HTTP_201_CREATED
)
async def create_node(data: schemas.NodeCreate, db: Session = Depends(get_db)):
    return PveService.create_node(db, data)


@pve_router.get("/nodes", response_model=List[schemas.NodeOut])
async def list_nodes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return PveService.list_nodes(db, skip, limit)


@pve_router.get("/nodes/{node_id}", response_model=schemas.NodeOut)
async def get_node(node_id: str, db: Session = Depends(get_db)):
    node_id = UUID(node_id)
    node = PveService.get_node(db, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@pve_router.patch("/nodes/{node_id}", response_model=schemas.NodeOut)
async def update_node(
    node_id: str, data: schemas.NodeUpdate, db: Session = Depends(get_db)
):
    node_id = UUID(node_id)
    updated = PveService.update_node(db, node_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Node not found")
    return updated


@pve_router.delete("/nodes/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_node(node_id: str, db: Session = Depends(get_db)):
    node_id = UUID(node_id)
    if not PveService.delete_node(db, node_id):
        raise HTTPException(status_code=404, detail="Node not found")


@pve_router.post(
    "/node-specs",
    response_model=schemas.NodeSpecsOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_node_specs(
    data: schemas.NodeSpecsCreate, db: Session = Depends(get_db)
):
    return PveService.create_node_specs(db, data)


@pve_router.get("/node-specs/{specs_id}", response_model=schemas.NodeSpecsOut)
async def get_node_specs(specs_id: int, db: Session = Depends(get_db)):
    specs = PveService.get_node_specs(db, specs_id)
    if not specs:
        raise HTTPException(status_code=404, detail="Specs not found")
    return specs


@pve_router.patch("/node-specs/{specs_id}", response_model=schemas.NodeSpecsOut)
async def update_node_specs(
    specs_id: int, data: schemas.NodeSpecsUpdate, db: Session = Depends(get_db)
):
    updated = PveService.update_node_specs(db, specs_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Specs not found")
    return updated


@pve_router.delete("/node-specs/{specs_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_node_specs(specs_id: int, db: Session = Depends(get_db)):
    if not PveService.delete_node_specs(db, specs_id):
        raise HTTPException(status_code=404, detail="Specs not found")


@pve_router.post(
    "/environments",
    response_model=schemas.NodeEnvironmentOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_environment(
    data: schemas.NodeEnvironmentCreate, db: Session = Depends(get_db)
):
    return PveService.create_node_environment(db, data)


@pve_router.get("/environments/{env_id}", response_model=schemas.NodeEnvironmentOut)
async def get_environment(env_id: int, db: Session = Depends(get_db)):
    env = PveService.get_node_environment(db, env_id)
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")
    return env


@pve_router.patch("/environments/{env_id}", response_model=schemas.NodeEnvironmentOut)
async def update_environment(
    env_id: int, data: schemas.NodeEnvironmentUpdate, db: Session = Depends(get_db)
):
    updated = PveService.update_node_environment(db, env_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Environment not found")
    return updated


@pve_router.delete("/environments/{env_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_environment(env_id: int, db: Session = Depends(get_db)):
    if not PveService.delete_node_environment(db, env_id):
        raise HTTPException(status_code=404, detail="Environment not found")


@pve_router.post(
    "/usage-logs",
    response_model=schemas.NodeUsageLogOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_usage_log(
    data: schemas.NodeUsageLogCreate, db: Session = Depends(get_db)
):
    return PveService.create_node_usage_log(db, data)


@pve_router.get("/usage-logs/{log_id}", response_model=schemas.NodeUsageLogOut)
async def get_usage_log(log_id: int, db: Session = Depends(get_db)):
    log = PveService.get_node_usage_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Usage log not found")
    return log


@pve_router.delete("/usage-logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usage_log(log_id: int, db: Session = Depends(get_db)):
    if not PveService.delete_node_usage_log(db, log_id):
        raise HTTPException(status_code=404, detail="Usage log not found")
