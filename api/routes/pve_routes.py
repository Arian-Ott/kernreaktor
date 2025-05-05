from fastapi import APIRouter, Depends, HTTPException

pve_router = APIRouter(prefix="/pve", tags=["PVE"])


@pve_router.get("/cluster")
async def get_cluster():
    """Get all clusters registered in the system."""
    return {"clusters": ["cluster1", "cluster2"]}


@pve_router.get("/cluster/{cluster_id}")
async def get_cluster_by_id(cluster_id: str):
    """Get a specific cluster by ID."""
    if cluster_id not in ["cluster1", "cluster2"]:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return {"cluster": cluster_id}


@pve_router.post("/cluster")
async def create_cluster(cluster_id: str):
    """Create a new cluster."""
    if cluster_id in ["cluster1", "cluster2"]:
        raise HTTPException(status_code=400, detail="Cluster already exists")
    return {"message": f"Cluster {cluster_id} created successfully"}


@pve_router.delete("/cluster/{cluster_id}")
async def delete_cluster(cluster_id: str):
    """Delete a specific cluster by ID."""
    if cluster_id not in ["cluster1", "cluster2"]:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return {"message": f"Cluster {cluster_id} deleted successfully"}


@pve_router.get("/nodes")
async def get_nodes():
    """Get all nodes in the system."""
    return {"nodes": ["node1", "node2"]}


@pve_router.get("/cluster/{cluster_id}/nodes")
async def get_nodes_by_cluster(cluster_id: str):
    """Get all nodes in a specific cluster."""
    if cluster_id not in ["cluster1", "cluster2"]:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return {"nodes": [f"node1-{cluster_id}", f"node2-{cluster_id}"]}


@pve_router.get("/cluster/{cluster_id}/nodes/{node_id}")
async def get_node_by_id(cluster_id: str, node_id: str):
    """Get a specific node by ID in a specific cluster."""
    if cluster_id not in ["cluster1", "cluster2"]:
        raise HTTPException(status_code=404, detail="Cluster not found")
    if node_id not in [f"node1-{cluster_id}", f"node2-{cluster_id}"]:
        raise HTTPException(status_code=404, detail="Node not found")
    return {"node": node_id}
