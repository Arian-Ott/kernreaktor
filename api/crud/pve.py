from sqlalchemy.orm import Session
from api.models.pve import Cluster, Node, NodeSpecs, NodeEnvironment, NodeUsageLog
from uuid import UUID

# ----------------------- Cluster -----------------------


def create_cluster(db: Session, cluster: Cluster) -> Cluster:
    db_cluster = Cluster(**cluster.model_dump())
    db.add(db_cluster)
    db.commit()
    db.refresh(db_cluster)
    return db_cluster


def get_cluster(db: Session, cluster_id: UUID) -> Cluster | None:
    return db.query(Cluster).filter(Cluster.id == cluster_id).first()


def get_clusters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cluster).offset(skip).limit(limit).all()


def update_cluster(db: Session, cluster_id: UUID, updates: dict) -> Cluster | None:
    db_cluster = get_cluster(db, cluster_id)
    if not db_cluster:
        return None
    for key, value in updates.items():
        setattr(db_cluster, key, value)
    db.commit()
    db.refresh(db_cluster)
    return db_cluster


def delete_cluster(db: Session, cluster_id: UUID) -> bool:
    db_cluster = get_cluster(db, cluster_id)
    if not db_cluster:
        return False
    db.delete(db_cluster)
    db.commit()
    return True


# ----------------------- Node -----------------------


def create_node(db: Session, node: Node) -> Node:
    db.add(node)
    db.commit()
    db.refresh(node)
    return node


def get_node(db: Session, node_id: UUID) -> Node | None:
    return db.query(Node).filter(Node.id == node_id).first()


def get_nodes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Node).offset(skip).limit(limit).all()


def update_node(db: Session, node_id: UUID, updates: dict) -> Node | None:
    db_node = get_node(db, node_id)
    if not db_node:
        return None
    for key, value in updates.items():
        setattr(db_node, key, value)
    db.commit()
    db.refresh(db_node)
    return db_node


def delete_node(db: Session, node_id: UUID) -> bool:
    db_node = get_node(db, node_id)
    if not db_node:
        return False
    db.delete(db_node)
    db.commit()
    return True


# ----------------------- NodeSpecs -----------------------


def create_node_specs(db: Session, specs: NodeSpecs) -> NodeSpecs:
    db.add(specs)
    db.commit()
    db.refresh(specs)
    return specs


def get_node_specs(db: Session, specs_id: int) -> NodeSpecs | None:
    return db.query(NodeSpecs).filter(NodeSpecs.id == specs_id).first()


def update_node_specs(db: Session, specs_id: int, updates: dict) -> NodeSpecs | None:
    db_specs = get_node_specs(db, specs_id)
    if not db_specs:
        return None
    for key, value in updates.items():
        setattr(db_specs, key, value)
    db.commit()
    db.refresh(db_specs)
    return db_specs


def delete_node_specs(db: Session, specs_id: int) -> bool:
    db_specs = get_node_specs(db, specs_id)
    if not db_specs:
        return False
    db.delete(db_specs)
    db.commit()
    return True


# ----------------------- NodeEnvironment -----------------------


def create_node_environment(db: Session, env: NodeEnvironment) -> NodeEnvironment:
    db.add(env)
    db.commit()
    db.refresh(env)
    return env


def get_node_environment(db: Session, env_id: int) -> NodeEnvironment | None:
    return db.query(NodeEnvironment).filter(NodeEnvironment.id == env_id).first()


def update_node_environment(
    db: Session, env_id: int, updates: dict
) -> NodeEnvironment | None:
    db_env = get_node_environment(db, env_id)
    if not db_env:
        return None
    for key, value in updates.items():
        setattr(db_env, key, value)
    db.commit()
    db.refresh(db_env)
    return db_env


def delete_node_environment(db: Session, env_id: int) -> bool:
    db_env = get_node_environment(db, env_id)
    if not db_env:
        return False
    db.delete(db_env)
    db.commit()
    return True


# ----------------------- NodeUsageLog -----------------------


def create_node_usage_log(db: Session, log: NodeUsageLog) -> NodeUsageLog:
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_node_usage_log(db: Session, log_id: int) -> NodeUsageLog | None:
    return db.query(NodeUsageLog).filter(NodeUsageLog.id == log_id).first()


def delete_node_usage_log(db: Session, log_id: int) -> bool:
    db_log = get_node_usage_log(db, log_id)
    if not db_log:
        return False
    db.delete(db_log)
    db.commit()
    return True
