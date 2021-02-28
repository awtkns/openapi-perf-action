<p align="center">
  <img src="https://openapi-perf.awtkns.com/assets/logo-light.png" alt="OpenAPI Perf Logo" />
</p>
<h3 align="center" style="margin-bottom: 0; color: black"><strong>OpenAPI Perf CI</strong></h3>
<p align="center">
  👷 <em> Continous Integration for OpenAPI-Perf </em> 👷</br>
  <sub>Automated OpenAPI Performance Testing and Reporting in Github</sub>
</p>
<p align="center">
<img alt="Tests" src="https://github.com/awtkns/openapi-perf/workflows/Tests/badge.svg" />
  <img alt="Tests" src="https://github.com/awtkns/openapi-perf-action/actions/workflows/integration.yml/badge.svg" />
<img alt="Docs" src="https://github.com/awtkns/fastapi-crudrouter/workflows/docs/badge.svg" />
</p>

---

**Documentation**: <a href="https://openapi-perf.awtkns.com/ci" target="_blank">https://openapi-perf.awtkns.com/ci</a>

**Source Code**: <a href="https://github.com/awtkns/openapi-perf-action" target="_blank">https://github.com/awtkns/openapi-perf-action</a>

**Github App**: <a href="https://github.com/apps/openapi-performance-testing" target="_blank">https://github.com/apps/openapi-performance-testing</a>

---

A github action for openapi-pref has been created to allow you to use openapi-perf in github workflows. Additionally, you can install the openapi-perf github app which will automatically comment and upload the generated report. Without the app installed, the report will be uploaded as a workflow artifact.

### Usage
```yaml
on: pull_request

jobs:
  openapi-perf:
    name: Builds and Runs the OpenAPI Performance Test Action
    if: ${{ github.event.issue.pull_request }}
    runs-on: ubuntu-latest
    steps:
    - name: OpenAPI Performance Test
      uses: awtkns/openapi-perf-action@main
      with:
        openapi-endpoint: 'http://localhost:5000/openapi.json'
```
