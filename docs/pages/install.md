# Install

## Install the plugins

Every plugin, with one command:

```bash
claude plugin marketplace add willoucom/ai
claude plugin install all@wj-plugins
```

[all](plugins/all.md) installs no component of its own: it depends on the
other plugins, and Claude Code installs them with it.

Or only the plugins you want:

```bash
claude plugin marketplace add willoucom/ai
claude plugin install wj@wj-plugins
claude plugin install wj-guard@wj-plugins
claude plugin install wj-behavior@wj-plugins
claude plugin install wj-code-style@wj-plugins
```

The plugins are installed in the `user` scope: their skills, hooks and output
style apply to every project of the machine.

## Update

The plugins have no `version`: every commit of the repository is a new
version.

In a Claude Code session, run `/plugin`, open the **Marketplaces** tab,
select `wj-plugins` and choose **Update marketplace**: it updates every plugin
you installed from it.

From your shell, update each plugin: updating `all@wj-plugins` updates `all`
alone, not the plugins it depends on.

```bash
claude plugin marketplace update wj-plugins
claude plugin update all@wj-plugins
claude plugin update wj@wj-plugins
claude plugin update wj-guard@wj-plugins
claude plugin update wj-behavior@wj-plugins
claude plugin update wj-code-style@wj-plugins
```

Updating `all@wj-plugins` installs a plugin added to it since; skip it if
you did not install `all`. The update applies at the next session, or after
`/reload-plugins`.

## Check

From the root of the repository:

```bash
claude plugin validate .
```
