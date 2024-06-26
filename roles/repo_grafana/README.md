# Ansible Role linuxfabrik.lfops.repo_grafana

This role deploys the Grafana OSS Repository.

Runs on

* RHEL 8 (and compatible)


## Tags

| Tag            | What it does                       |
| ---            | ------------                       |
| `repo_grafana` | Deploys the Grafana OSS Repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_grafana__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_grafana__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
