"""
Module to hold the request handlers.
"""
import json
import urllib

from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from parallel_run.handlers import DuckDuckGo, Google, Twitter
from parallel_run.worker import WorkerManager


class SearchAPI(View):

    def get(self, request):
        """
        Method to handle search api's HTTP GET requests.
        """

        q = request.GET.get("q")
        if not q:
            return JsonResponse({"message": "No query string found"})

        result = {"query": q, "result": {}}

        data = self._make_worker_request(q)
        for res in data:
            result["result"].update(res)

        return HttpResponse(
            json.dumps(result, indent=4),
            content_type="application/json"
        )

    def _make_worker_request(self, q):
        """
        Method to call the workers to run in parallel.

        :param q: Actual query string requested
        """
        q = urllib.parse.quote(q)
        requests = [DuckDuckGo(q), Google(q), Twitter(q)]

        # Worker count can be automated and provided in the request
        worker_manager = WorkerManager(requests, worker_count=3)

        return worker_manager.distribute()
