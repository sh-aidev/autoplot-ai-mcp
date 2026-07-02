"""
`get_datasets_list` tool: keyword search over a configured data source's datasets.

Different sources expose entirely different discovery APIs (paginated GET vs.
search-index POST, differing response shapes), so fetching is dispatched per
`ApiSource.type` to a dedicated `_fetch_<type>` method, each returning a common
`{id, name, description, source}` shape for the tool to return.
"""

import requests
from mcp.server.fastmcp import FastMCP

from src.utils.config import Config
from src.utils.exceptions import ToolExecutionError
from src.utils.logger import logger
from src.utils.models import ApiSource


class DatasetDiscoveryTool:
    """
    Registers and implements the `get_datasets_list` tool.
    """

    def __init__(self, config: Config) -> None:
        """
        Args:
            config (Config): Loaded application configuration.
        """
        self.config = config

    def get_api_source(self, source: str) -> ApiSource:
        """
        Looks up a configured API source by name.

        Args:
            source (str): Name of the data source to look up (e.g. "world_bank").

        Returns:
            ApiSource: The matching API source configuration.

        Raises:
            ToolExecutionError: If no configured source matches `source`.
        """
        for api in self.config.app_config.apis:
            if api.name == source:
                return api
        raise ToolExecutionError(
            f"Unknown data source '{source}'. Configured sources: "
            f"{[api.name for api in self.config.app_config.apis]}"
        )

    def _fetch_world_bank_v2(self, api: ApiSource, keywords: list[str]) -> list[dict]:
        """
        Fetches and keyword-filters datasets from a World Bank V2-shaped API.

        The V2 indicator API has no server-side search, so this pages through
        every indicator and filters locally.

        Args:
            api (ApiSource): The API source to query.
            keywords (list[str]): Keywords to match against name/description.

        Returns:
            list[dict]: Matching datasets, name-matches ranked above
                        description-matches, shorter names first.
        """
        name_matches: list[dict] = []
        description_matches: list[dict] = []
        page = 1
        keywords_lower = [keyword.lower() for keyword in keywords]
        while True:
            resp = requests.get(
                api.discovery_endpoint,
                params={"format": api.format, "per_page": api.per_page, "page": page},
                timeout=15,
            )
            resp.raise_for_status()
            meta, indicators = resp.json()

            for indicator in indicators:
                name = indicator.get("name", "")
                description = indicator.get("sourceNote", "")
                dataset = {
                    "id": indicator["id"],
                    "name": name,
                    "description": description,
                    "source": api.name,
                }
                name_lower = name.lower()
                description_lower = description.lower()
                if not keywords_lower:
                    name_matches.append(dataset)
                elif any(keyword in name_lower for keyword in keywords_lower):
                    name_matches.append(dataset)
                elif any(keyword in description_lower for keyword in keywords_lower):
                    description_matches.append(dataset)

            if page >= meta["pages"]:
                break
            page += 1

        # Datasets whose name mentions a keyword rank above ones that only
        # mention it in the (much longer, noisier) description. Within a
        # tier, shorter names tend to be the general/canonical indicator
        # (e.g. "Population, total") rather than a narrow derived one.
        name_matches.sort(key=lambda d: len(d["name"]))
        description_matches.sort(key=lambda d: len(d["name"]))
        return name_matches + description_matches

    def _fetch_data360(self, api: ApiSource, keywords: list[str], limit: int) -> list[dict]:
        """
        Searches datasets from a Data360-shaped API via its `searchv2` index.

        Unlike the V2 API, Data360's search is server-side, so keywords are
        sent as the search term and results come back pre-ranked; no local
        filtering or sorting is needed.

        Args:
            api (ApiSource): The API source to query.
            keywords (list[str]): Keywords to search for.
            limit (int): Maximum number of results to request.

        Returns:
            list[dict]: Matching datasets in the order returned by the API.
                        `description` is left empty: Data360's `searchv2`
                        response schema is undocumented beyond
                        `series_description/{idno,name,database_id}`, so no
                        description field is fetched.
        """
        resp = requests.post(
            api.discovery_endpoint,
            json={
                "search": " ".join(keywords) if keywords else "*",
                "select": "series_description/idno, series_description/name, series_description/database_id",
                "top": limit,
                "count": True,
            },
            timeout=15,
        )
        resp.raise_for_status()
        results = resp.json().get("value", [])

        matches: list[dict] = []
        for result in results:
            series = result.get("series_description", {})
            matches.append(
                {
                    "id": series.get("idno"),
                    "name": series.get("name", ""),
                    "description": "",
                    "source": api.name,
                }
            )
        return matches

    def register(self, mcp: FastMCP) -> None:
        """
        Registers the `get_datasets_list` tool on the given FastMCP server.

        Args:
            mcp (FastMCP): The MCP server instance to register the tool on.
        """

        @mcp.tool()
        def get_datasets_list(
            keywords: list[str] = [], source: str = "world_bank", limit: int = 15
        ) -> list[dict]:
            """
            Step 1 of the data pipeline. Lists datasets available from the
            configured data source, each with an id and a human-readable
            description. Use `keywords` to narrow the results to the terms or
            topics relevant to what the user asked for (each keyword is
            matched against each dataset's name and description). Read the
            returned descriptions and pick the single best-matching dataset
            id, then pass it to `download_dataset` next.

            Args:
                keywords (list[str]): List of keywords to filter datasets.
                source (str): The data source to query (default: "world_bank").
                limit (int): Maximum number of datasets to return (default: 15).

            Returns:
                list[dict]: A list of dictionaries, each containing the dataset's
                            id, name, description, and source.
            """
            api = self.get_api_source(source)
            logger.debug(f"Listing datasets from '{source}' (keywords={keywords!r})")

            if api.type == "world_bank_v2":
                matches = self._fetch_world_bank_v2(api, keywords)
            elif api.type == "data360":
                matches = self._fetch_data360(api, keywords, limit)
            else:
                raise ToolExecutionError(
                    f"Unsupported API type '{api.type}' for source '{source}'"
                )

            logger.debug(f"Found {len(matches)} matching datasets, returning up to {limit}")
            return matches[:limit]
