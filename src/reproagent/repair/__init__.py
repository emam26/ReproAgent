"""Controlled repair-action and experiment foundation."""

from .engine import RepairExperimentEngine
from .models import (
    RepairAction,
    RepairActionType,
    RepairExperimentResult,
    RepairExperimentStatus,
    RepairLimits,
    RepairObservation,
    RepairRisk,
    Reversibility,
)
from .plan import AppliedPlanRepair, PlanRepairApplier, RepairNotExecutableError
from .policy import RepairPolicyError, validate_repair_action

__all__ = [
    "AppliedPlanRepair",
    "PlanRepairApplier",
    "RepairAction",
    "RepairActionType",
    "RepairExperimentEngine",
    "RepairExperimentResult",
    "RepairExperimentStatus",
    "RepairLimits",
    "RepairNotExecutableError",
    "RepairObservation",
    "RepairPolicyError",
    "RepairRisk",
    "Reversibility",
    "validate_repair_action",
]
