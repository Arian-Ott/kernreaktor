import uuid
from sqlalchemy.orm import Session
from api.crud import nodes
from api.schemas.nodes import (
    EnvironmentCreate,
    StatusSnapshotCreate,
    VMConfigCreate,
    LXCConfigCreate,
)


def test_create_environment(db: Session):
    env_data = EnvironmentCreate(
        vmid=100,
        name="test-vm",
        type="qemu",
        node_name="pve1",
        os_type="linux",
        ip_address="192.168.1.100",
        template=False,
        tags="dev",
    )
    env = nodes.create_environment(db, env_data)
    assert env.vmid == 100
    assert env.name == "test-vm"
    assert env.type.value == "qemu"
    assert env.node_name == "pve1"


def test_create_vm_config(db: Session):
    # Create environment first
    env = nodes.create_environment(
        db,
        EnvironmentCreate(
            vmid=101,
            name="vm-config-test",
            type="qemu",
            node_name="pve1",
            os_type="linux",
        ),
    )
    config = nodes.create_vm_config(
        db, env.id, "seabios", "pc", "virtio-scsi-pci", "debian.iso", "cdn"
    )
    assert config.environment_id == env.id
    assert config.bios == "seabios"


def test_create_lxc_config(db: Session):
    env = nodes.create_environment(
        db,
        EnvironmentCreate(
            vmid=102,
            name="lxc-config-test",
            type="lxc",
            node_name="pve1",
            os_type="debian",
        ),
    )
    config = nodes.create_lxc_config(db, env.id, "/dev/data", "mnt/data", "nesting=1")
    assert config.environment_id == env.id
    assert config.rootfs == "/dev/data"


def test_create_status_snapshot(db: Session):
    env = nodes.create_environment(
        db,
        EnvironmentCreate(
            vmid=103,
            name="snapshot-test",
            type="qemu",
            node_name="pve1",
            os_type="ubuntu",
        ),
    )
    snapshot_data = StatusSnapshotCreate(
        status="running",
        uptime=12000,
        cpu_usage=0.25,
        memory_used=2048000,
        memory_total=4096000,
        disk_used=50000000,
        disk_total=100000000,
        netin_bytes=1048576,
        netout_bytes=2048576,
    )
    snapshot = nodes.create_status_snapshot(db, snapshot_data, env.id)
    assert snapshot.environment_id == env.id
    assert snapshot.status == "running"
    assert snapshot.cpu_usage == 0.25
