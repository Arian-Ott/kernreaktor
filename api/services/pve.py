from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from api.schemas import pve as schemas
from api.crud import pve as crud


class PveService:
    @staticmethod
    def create_cluster(db: Session, data: schemas.ClusterCreate):
        return crud.create_cluster(db, data)

    @staticmethod
    def get_cluster(db: Session, cluster_id: UUID):
        return crud.get_cluster(db, cluster_id)

    @staticmethod
    def list_clusters(db: Session, skip: int = 0, limit: int = 100):
        return crud.get_clusters(db, skip, limit)

    @staticmethod
    def update_cluster(db: Session, cluster_id: UUID, data: schemas.ClusterUpdate):
        return crud.update_cluster(db, cluster_id, data)

    @staticmethod
    def delete_cluster(db: Session, cluster_id: UUID):
        return crud.delete_cluster(db, cluster_id)

    @staticmethod
    def create_node(db: Session, data: schemas.NodeCreate):
        return crud.create_node(db, data)

    @staticmethod
    def get_node(db: Session, node_id: UUID):
        return crud.get_node(db, node_id)

    @staticmethod
    def list_nodes(db: Session, skip: int = 0, limit: int = 100):
        return crud.get_nodes(db, skip, limit)

    @staticmethod
    def update_node(db: Session, node_id: UUID, data: schemas.NodeUpdate):
        return crud.update_node(db, node_id, data)

    @staticmethod
    def delete_node(db: Session, node_id: UUID):
        return crud.delete_node(db, node_id)

    @staticmethod
    def create_node_specs(db: Session, data: schemas.NodeSpecsCreate):
        return crud.create_node_specs(db, data)

    @staticmethod
    def get_node_specs(db: Session, specs_id: int):
        return crud.get_node_specs(db, specs_id)

    @staticmethod
    def update_node_specs(db: Session, specs_id: int, data: schemas.NodeSpecsUpdate):
        return crud.update_node_specs(db, specs_id, data)

    @staticmethod
    def delete_node_specs(db: Session, specs_id: int):
        return crud.delete_node_specs(db, specs_id)

    # ----------------------- NodeEnvironment -----------------------

    @staticmethod
    def create_node_environment(db: Session, data: schemas.NodeEnvironmentCreate):
        return crud.create_node_environment(db, data)

    @staticmethod
    def get_node_environment(db: Session, env_id: int):
        return crud.get_node_environment(db, env_id)

    @staticmethod
    def update_node_environment(
        db: Session, env_id: int, data: schemas.NodeEnvironmentUpdate
    ):
        return crud.update_node_environment(db, env_id, data)

    @staticmethod
    def delete_node_environment(db: Session, env_id: int):
        return crud.delete_node_environment(db, env_id)

    @staticmethod
    def create_node_usage_log(db: Session, data: schemas.NodeUsageLogCreate):
        return crud.create_node_usage_log(db, data)

    @staticmethod
    def get_node_usage_log(db: Session, log_id: int):
        return crud.get_node_usage_log(db, log_id)

    @staticmethod
    def delete_node_usage_log(db: Session, log_id: int):
        return crud.delete_node_usage_log(db, log_id)
