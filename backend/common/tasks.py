"""
Background task definitions for Cartify foundation.
Provides minimal verification tasks for Celery worker and Redis broker health.
"""
import logging
from celery import shared_task

logger = logging.getLogger('cartify.tasks')


@shared_task(bind=True, name="common.health_check_task")
def health_check_task(self):
    """
    Minimal asynchronous diagnostic task.
    Verifies Celery task registration, message broker dispatch via Redis,
    and worker execution.
    """
    task_id = self.request.id or "direct_execution"
    logger.info("Executing Celery health check task. Task ID: %s", task_id)
    return {
        "status": "success",
        "task_id": task_id,
        "message": "Celery worker and Redis broker operational",
    }
