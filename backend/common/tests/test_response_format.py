"""Tests for standardized API response structures and pagination envelope."""
from django.test import TestCase, RequestFactory
from django.core.paginator import Paginator
from rest_framework import status
from common.responses import success_response, error_response
from common.pagination import StandardResultsSetPagination


class ResponseFormatTests(TestCase):
    """Tests verifying the Cartify standard API response format."""

    def test_success_response_structure_default(self):
        """Verify default success response envelope."""
        response = success_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "success": True,
                "message": "Request successful",
                "data": {},
            },
        )

    def test_success_response_with_custom_data_and_message(self):
        """Verify success response with custom data payload and message."""
        payload_data = {"item_id": 42, "status": "active"}
        response = success_response(
            data=payload_data,
            message="Item retrieved successfully",
            status_code=status.HTTP_201_CREATED,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Item retrieved successfully")
        self.assertEqual(response.data["data"], payload_data)

    def test_error_response_structure_default(self):
        """Verify default error response envelope."""
        response = error_response()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "success": False,
                "message": "Something went wrong",
                "errors": {},
            },
        )

    def test_error_response_with_custom_errors_and_message(self):
        """Verify error response with specific validation errors."""
        field_errors = {"email": ["Enter a valid email address."]}
        response = error_response(
            errors=field_errors,
            message="Invalid input data",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "Invalid input data")
        self.assertEqual(response.data["errors"], field_errors)

    def test_paginated_response_structure(self):
        """Verify StandardResultsSetPagination wraps results in the standard success envelope."""
        pagination = StandardResultsSetPagination()
        factory = RequestFactory()
        request = factory.get('/api/v1/test/?page=1&page_size=2')

        dataset = [{"id": 1}, {"id": 2}, {"id": 3}]
        paginator = Paginator(dataset, 2)
        page = paginator.page(1)
        pagination.page = page
        pagination.request = request

        response = pagination.get_paginated_response([{"id": 1}, {"id": 2}])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Request successful")
        self.assertEqual(response.data["data"]["count"], 3)
        self.assertIsNotNone(response.data["data"]["next"])
        self.assertIsNone(response.data["data"]["previous"])
        self.assertEqual(response.data["data"]["results"], [{"id": 1}, {"id": 2}])
