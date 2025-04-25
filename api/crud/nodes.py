from sqlalchemy.orm import Session
from api.models.environment import (
    Environment,
    VMConfig,
    LXCConfig,
    StatusSnapshot,
    VMType,
)
from api.schemas.nodes import EnvironmentCreate, StatusSnapshotCreate
import uuid


def create_environment(db: Session, env_data: EnvironmentCreate) -> Environment:
    env = Environment(
        id=uuid.uuid4(),
        vmid=env_data.vmid,
        name=env_data.name,
        type=env_data.type,
        node_name=env_data.node_name,
        os_type=env_data.os_type,
        ip_address=env_data.ip_address,
        template=env_data.template,
        tags=env_data.tags,
    )
    db.add(env)
    db.commit()
    db.refresh(env)
    return env


def get_environment_by_vmid(db: Session, vmid: int) -> Environment:
    return db.query(Environment).filter(Environment.vmid == vmid).first()


def get_all_environments(db: Session):
    return db.query(Environment).all()


def create_vm_config(
    db: Session,
    environment_id: str,
    bios: str,
    machine: str,
    scsihw: str,
    iso: str,
    boot_order: str,
) -> VMConfig:
    config = VMConfig(
        id=uuid.uuid4(),
        environment_id=environment_id,
        bios=bios,
        machine=machine,
        scsihw=scsihw,
        iso=iso,
        boot_order=boot_order,
    )
    db.add(config)
    db.commit()
    db.refresh(config)
    return config


def create_lxc_config(
    db: Session, environment_id: str, rootfs: str, mounts: str, features: str
) -> LXCConfig:
    config = LXCConfig(
        id=uuid.uuid4(),
        environment_id=environment_id,
        rootfs=rootfs,
        mounts=mounts,
        features=features,
    )
    db.add(config)
    db.commit()
    db.refresh(config)
    return config


def create_status_snapshot(
    db: Session, snapshot_data: StatusSnapshotCreate, environment_id: str
) -> StatusSnapshot:
    snapshot = StatusSnapshot(
        environment_id=environment_id,
        status=snapshot_data.status,
        uptime=snapshot_data.uptime,
        cpu_usage=snapshot_data.cpu_usage,
        memory_used=snapshot_data.memory_used,
        memory_total=snapshot_data.memory_total,
        disk_used=snapshot_data.disk_used,
        disk_total=snapshot_data.disk_total,
        netin_bytes=snapshot_data.netin_bytes,
        netout_bytes=snapshot_data.netout_bytes,
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot
