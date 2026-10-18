# Install

## Install the plugin

```bash
claude plugin marketplace add willoucom/ai
claude plugin install wj@wj-plugins
```

The plugin is installed in the `user` scope: its skills, hooks and output
style apply to every project of the machine.

## Update

The plugin has no `version`: every commit of the repository is a new
version.

In a Claude Code session, run `/plugin`, open the **Marketplaces** tab,
select `wj-plugins` and choose **Update marketplace**: it updates every plugin
you installed from it.

From your shell:

```bash
claude plugin marketplace update wj-plugins
claude plugin update wj@wj-plugins
```

The update applies at the next session, or after `/reload-plugins`.

## Check

From the root of the repository:

```bash
claude plugin validate .
```
