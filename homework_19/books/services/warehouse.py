import logging
import os

import requests

logger = logging.getLogger(__name__)

WAREHOUSE_API_URL = os.getenv(
    "WAREHOUSE_API_URL",
    "http://warehouse_nginx",
)


class WarehouseServiceError(Exception):
    """Warehouse service is unavailable."""


class InventoryNotFoundError(Exception):
    """Inventory was not found for the product."""


def get_inventory(product_id, authorization=None):
    url = f"{WAREHOUSE_API_URL}/api/inventory/"

    headers = {}

    if authorization:
        headers["Authorization"] = authorization

    try:
        response = requests.get(
            url,
            params={"product_id": product_id},
            headers=headers,
            timeout=5,
        )
        response.raise_for_status()

        inventory = response.json()

        if not isinstance(inventory, list):
            logger.error(
                "Unexpected warehouse response for product_id=%s",
                product_id,
            )
            raise WarehouseServiceError

        if not inventory:
            logger.warning(
                "Inventory not found for product_id=%s",
                product_id,
            )
            raise InventoryNotFoundError(product_id)

        return inventory[0]

    except InventoryNotFoundError:
        raise

    except requests.RequestException as exc:
        logger.exception(
            "Warehouse API request failed for product_id=%s",
            product_id,
        )
        raise WarehouseServiceError from exc

    except (ValueError, TypeError) as exc:
        logger.exception(
            "Invalid JSON response from Warehouse API " "for product_id=%s",
            product_id,
        )
        raise WarehouseServiceError from exc
