from enum import Enum
from typing import List, Set
from fastapi import HTTPException, status


class Role(str, Enum):
    WORKER = "WORKER"
    SUPERVISOR = "SUPERVISOR"
    CONTROL_ROOM = "CONTROL_ROOM"
    ADMIN = "ADMIN"
    AUDITOR = "AUDITOR"


# Explicit Role Permission Definitions (Section 24)
ROLE_PERMISSIONS: dict[Role, Set[str]] = {
    Role.WORKER: {
        "worker:view_self",
        "alert:ack_own",
        "emergency:trigger",
        "system:read_health",
    },
    Role.SUPERVISOR: {
        "worker:view_self",
        "worker:view_team",
        "alert:ack_own",
        "alert:ack_team",
        "alert:escalate",
        "emergency:trigger",
        "system:read_health",
    },
    Role.CONTROL_ROOM: {
        "worker:view_all",
        "alert:ack_all",
        "alert:escalate_all",
        "emergency:trigger",
        "emergency:manage",
        "incident:view_all",
        "system:read_health",
    },
    Role.AUDITOR: {
        "worker:view_all",
        "alert:view_all",
        "audit:read_logs",
        "system:read_health",
    },
    Role.ADMIN: {
        "worker:view_all",
        "worker:manage",
        "alert:view_all",
        "alert:ack_all",
        "audit:read_logs",
        "config:manage",
        "users:manage",
        "system:read_health",
    },
}


class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, user_role: str) -> bool:
        try:
            role_enum = Role(user_role.upper())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Invalid role: {user_role}",
            )

        granted_permissions = ROLE_PERMISSIONS.get(role_enum, set())
        if self.required_permission not in granted_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user_role}' lacks required permission '{self.required_permission}'",
            )
        return True
