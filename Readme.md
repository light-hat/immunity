<p align="center">
<img alt="Logo" src="frontend/public/favicon_gray.png" height="150px">
</p>

<h1 align="center">Immunity</h1>
<p align="center">
Interactive Analysis Platform for Distributed Debugging and Security Testing (IAST, SCA). 
</p>

<p align="center">
<img alt="Codecov" src="https://img.shields.io/codecov/c/github/light-hat/immunity.svg">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<img alt="Python version" src="https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white">
<img alt="Django" src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green&style=flat">
<img alt="Node version" src="https://img.shields.io/badge/Node.js-20+-339933?logo=node.js&logoColor=white&style=flat">
<img alt="Vue" src="https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D&style=flat">
<a href="https://github.com/light-hat/smart_ids/actions"><img alt="Pipeline status" src="https://github.com/light-hat/immunity/workflows/CodeQL/badge.svg"></a>
<a href="https://github.com/light-hat/smart_ids/actions"><img alt="Pipeline status" src="https://github.com/light-hat/immunity/workflows/Build%20&%20Push%20Docker%20Image/badge.svg"></a>
<a href="https://github.com/light-hat/smart_ids/actions"><img alt="Pipeline status" src="https://github.com/light-hat/immunity/workflows/Unit%20Test/badge.svg"></a>
<a href="https://github.com/light-hat/smart_ids/actions"><img alt="Pipeline status" src="https://github.com/light-hat/immunity/workflows/Build%20&%20Deploy%20Documentation/badge.svg"></a>
</p>

<img alt="DEMO" src="assets/demo.gif">

## Stats

![Alt](https://repobeats.axiom.co/api/embed/60164b1bae35c9b96114fbddcd887eef0515959a.svg "Repobeats analytics image")

## Concept

```mermaid
sequenceDiagram
loop Runtime
Automated Tests/DAST/Fuzzing->>Your App with Agent: HTTP-request
Your App with Agent->>Management server: Runtime data
Your App with Agent-->>Automated Tests/DAST/Fuzzing: HTTP-response
end
DevSecOps/AppSec->>Management server: Requesting a list of vulnerabilities
Management server-->>DevSecOps/AppSec: List of found vulnerabilities

```

## Related projects

| Name                  | Type       | Description                                                        | URL                                                                                                      |
| --------------------- | ---------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| immunity-python-agent | IAST agent | IAST agent for interactive analysis of web applications in Python. | [https://github.com/light-hat/immunity-python-agent](https://github.com/light-hat/immunity-python-agent) |

## Server requirements

| Parameter | Standalone                | Cluster            | ML mode            |
|-----------|---------------------------|--------------------|--------------------|
| OS        | ...   |      ...              |            ...        |
| CPU       | ...                  |         ...           |         ...           |
| RAM       | ...                     |         ...           |     ...               |
| GPU       | ...       |        ...            |      ...              |

## Screenshots

...
