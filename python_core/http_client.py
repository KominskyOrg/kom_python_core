import logging
import requests
from requests.exceptions import (
    ConnectionError,
    Timeout,
    HTTPError,
    RequestException,
)

logger = logging.getLogger(__name__)

class HTTPClient:
    def __init__(self, base_url, timeout=5):
        """
        Initialize the HTTP client.

        :param base_url: The base URL for the HTTP client.
        :param timeout: Timeout for HTTP requests in seconds.
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def make_request(self, method, endpoint, data=None, headers=None):
        """
        Make an HTTP request and handle exceptions.

        :param method: HTTP method (e.g., 'GET', 'POST').
        :param endpoint: API endpoint (appended to base_url).
        :param data: JSON data to send in the request.
        :param headers: Dictionary of HTTP headers to send with the request.
        :return: Tuple of (response_data, status_code).
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"Making {method} request to {url} with data: {data} and headers: {headers}")

        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            logger.debug(f"Received response with status code {response.status_code} from {url}")

            try:
                response_data = response.json()
            except ValueError:
                logger.error(f"Invalid JSON response from {url}")
                response_data = {"message": "Invalid response from service"}
                return response_data, 502  # Bad Gateway

            # Check response status code
            if 200 <= response.status_code < 300:
                logger.debug(f"Successful response from {url}: {response_data}")
                return response_data, response.status_code
            elif 400 <= response.status_code < 500:
                # Client error; pass through the response
                error_message = response_data.get("message", "Client error")
                logger.warning(f"Client error from {url}: {error_message}")
                json_response = {"message": error_message}
                logger.debug(f"Returning JSON response: {json_response}")
                return json_response, response.status_code
            elif 500 <= response.status_code < 600:
                # Server error; return 503 Service Unavailable
                logger.error(f"Server error from {url}: {response_data}")
                return {"message": "Service encountered an error"}, 503
            else:
                logger.error(f"Unexpected status code {response.status_code} from {url}")
                return {"message": "Unexpected response from service"}, 502

        except (ConnectionError, Timeout) as e:
            logger.error(f"Connection error when connecting to {url}: {e}")
            return {"message": "Service is unavailable"}, 503
        except HTTPError as e:
            logger.error(f"HTTP error when connecting to {url}: {e}")
            return {"message": "HTTP error occurred"}, 502
        except RequestException as e:
            logger.error(f"Request exception when connecting to {url}: {e}")
            return {"message": "An error occurred while connecting to service"}, 502
        except Exception as e:
            # Catch-all for any other exceptions
            logger.exception(f"Unexpected error when connecting to {url}: {e}")
            return {"message": "Internal server error"}, 500
