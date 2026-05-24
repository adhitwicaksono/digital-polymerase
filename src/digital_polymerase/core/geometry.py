"""Coordinate geometry utilities."""
from __future__ import annotations
from typing import Iterable
import numpy as np

def as_coord_array(coords) -> np.ndarray:
    arr = np.asarray(coords, dtype=float)
    if arr.shape != (3,): raise ValueError(f"Expected coordinate shape (3,), got {arr.shape}")
    return arr

def distance(a, b) -> float: return float(np.linalg.norm(as_coord_array(a) - as_coord_array(b)))

def centroid(points) -> np.ndarray:
    arr = np.asarray(list(points), dtype=float)
    if arr.ndim != 2 or arr.shape[1] != 3 or arr.shape[0] == 0: raise ValueError(f"Expected (n,3), got {arr.shape}")
    return arr.mean(axis=0)

def rmsd(a, b) -> float:
    a = np.asarray(a, dtype=float); b = np.asarray(b, dtype=float)
    if a.shape != b.shape: raise ValueError(f"RMSD arrays differ: {a.shape} vs {b.shape}")
    return float(np.sqrt(np.mean(np.sum((a-b)**2, axis=1))))

def kabsch(mobile, target):
    mobile = np.asarray(mobile, dtype=float); target = np.asarray(target, dtype=float)
    if mobile.shape != target.shape: raise ValueError("Kabsch arrays must have the same shape")
    if mobile.ndim != 2 or mobile.shape[1] != 3 or mobile.shape[0] < 3: raise ValueError("Kabsch requires at least 3 paired 3D points")
    mc = mobile.mean(axis=0); tc = target.mean(axis=0)
    m = mobile - mc; t = target - tc
    u, _s, vt = np.linalg.svd(m.T @ t)
    r = vt.T @ u.T
    if np.linalg.det(r) < 0: vt[-1,:] *= -1; r = vt.T @ u.T
    tr = tc - r @ mc
    fitted = (r @ mobile.T).T + tr
    return r, tr, rmsd(fitted, target)

def apply_transform(coords, rotation, translation):
    coords = np.asarray(coords, dtype=float)
    if coords.shape == (3,): return rotation @ coords + translation
    if coords.ndim == 2 and coords.shape[1] == 3: return (rotation @ coords.T).T + translation
    raise ValueError(f"Expected (3,) or (n,3), got {coords.shape}")

def angle(a,b,c) -> float:
    ba = as_coord_array(a)-as_coord_array(b); bc = as_coord_array(c)-as_coord_array(b)
    den = np.linalg.norm(ba)*np.linalg.norm(bc)
    if den == 0: raise ValueError("zero-length vector")
    return float(np.degrees(np.arccos(np.clip(np.dot(ba,bc)/den, -1.0, 1.0))))

def dihedral(a,b,c,d) -> float:
    p0,p1,p2,p3 = map(as_coord_array, [a,b,c,d])
    b0 = -(p1-p0); b1 = p2-p1; b2 = p3-p2
    n = np.linalg.norm(b1)
    if n == 0: raise ValueError("zero-length central bond")
    b1 = b1/n
    v = b0 - np.dot(b0,b1)*b1; w = b2 - np.dot(b2,b1)*b1
    return float(np.degrees(np.arctan2(np.dot(np.cross(b1,v),w), np.dot(v,w))))
